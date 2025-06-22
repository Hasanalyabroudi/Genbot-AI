

import uuid
import numpy as np
import pyodbc  
import base64
import ast
from collections import Counter, defaultdict
import math
import psycopg2
import psycopg2.extras
import re
import os 
from psycopg2.extras import execute_values
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv 
from tqdm import tqdm
import pandas as pd


 
psycopg2.extras.register_uuid()


class db:
   def __init__(self, SERVER_IP,DATABASE_NAME,username, password):

      self.SERVER_IP = SERVER_IP
      self.DATABASE_NAME = DATABASE_NAME
      self.username = username
      self.password = password

    #Conection to Azure Database
   def connect(self,attempt=0,max_attempts=3):
      if attempt == max_attempts:
         print("Max attempts reached")
         return

      try:
         self.conn = psycopg2.connect(
            database=   self.DATABASE_NAME,
            user= self.username,
            password= self.password,
            host= self.SERVER_IP,
            port= '5432'
         ) 
         self.conn.autocommit = True  #  Disable transactions for DB creation


      
      except Exception as e:

         if 'does not exist' in str(e):
            print(f"Database {self.DATABASE_NAME} not found")
            ## Create the database
            self.CreateDB()

            ## Connect to the database again
            self.connect(attempt=attempt+1)
            ##
            self.CreateIDxURLTable()
            self.CreateIDxWordTable()
            self.CreateURLxFreqTable()
            self.CreateWORDxURLxFreqTable()
            self.CreateIDxTotalURLS()
            self.CreateURLxTotalWORDS()
            self.CreateTF_IDF()
            
         else:
            print(f"Failed to connect to the database: {e}")
            raise

      ## autocommit
      # self.conn.autocommit = True

      #Creating a cursor object using the cursor() method
      self.cursor = self.conn.cursor()

      
      

      

      print(f"Connected to SQL Database {self.DATABASE_NAME}")


   def CloseConnection(self):
      self.conn.close()
   
 
    ### Database Setup
    # Create Words Table For AzureSQL


    ## Creating new DB
   def CreateDB(self):
      '''
      Create a new database
      To do so will connect using the default database 'postgres' and then create a new database
      '''
      conn = psycopg2.connect(
            database= 'postgres',
            user= self.username,
            password= self.password,
            host= self.SERVER_IP,
            port= '5432'
         )
      # conn.autocommit = True
   #Creating a cursor object using the cursor() method
      cursor = conn.cursor()
      print("Connected to SQL Database using default database 'postgres'")
      conn.autocommit = True
      
      # Create a new database
      cursor.execute(f"CREATE DATABASE {self.DATABASE_NAME}")
      print(f"Database {self.DATABASE_NAME} created successfully")
      
      conn.close()
      print("Connection closed")
        

    ##Create tables-------

   def CreateIDxURLTable(self):
      self.cursor.execute("""CREATE TABLE IDxURL (
                      ID UUID PRIMARY KEY,
                      URL TEXT NOT NULL UNIQUE
                      );""")    
      self.conn.commit()
      print("Table IDxURL Created")


   def CreateIDxWordTable(self):
      self.cursor.execute("""CREATE TABLE IDxWord (
                     ID UUID PRIMARY KEY,
                     WORD TEXT NOT NULL UNIQUE
                     );""")
      self.conn.commit()
      print("Table IDxWord Created")

   def CreateURLxFreqTable(self):
      self.cursor.execute("""CREATE TABLE URLxFreq (
                     IDurl UUID PRIMARY KEY REFERENCES IDxURL(ID),
                     Freq FLOAT NOT NULL
                     );""")
      self.conn.commit()
      print("Table URLxFreq Created")

   def CreateWORDxURLxFreqTable(self):
      self.cursor.execute("""CREATE TABLE WORDxURLxFreq (
                     IDurl UUID NOT NULL REFERENCES IDxURL(ID),
                     IDword UUID NOT NULL REFERENCES IDxWord(ID),
                     Frequency INT NOT NULL,
                     PRIMARY KEY (IDurl, IDword)
                     );""")
      self.conn.commit()
      print("Table WORDxURLxFreq Created")


   def CreateIDxTotalURLS(self):
      self.DropTable('IDxTotalURLs')
      
      self.cursor.execute("""CREATE TABLE IDxTotalURLs (
                           IDword UUID PRIMARY KEY,
                           URLcount INT NOT NULL
                           );""")
      self.conn.commit()
      print("Table IDxTotalURLs Created")

      self.cursor.execute("""INSERT INTO IDxTotalURLs (IDword, URLcount)
                           SELECT 
                              IDword,
                              COUNT(DISTINCT IDurl) AS URLcount
                           FROM 
                              WORDxURLxFreq
                           GROUP BY 
                              IDword;""")
      self.conn.commit()
      print("Table IDxTotalURLs Populated")

   def CreateURLxTotalWORDS(self):
      self.DropTable('URLxTotalWORDS')
      self.cursor.execute("""CREATE TABLE URLxTotalWORDS (
                           IDurl UUID PRIMARY KEY,
                           Wordcount INT NOT NULL
                           );""")
      self.conn.commit()
      print("Table URLxTotalWORDS Created")

      self.cursor.execute("""INSERT INTO URLxTotalWORDS (IDurl, Wordcount)
                           SELECT 
                              IDurl,
                              SUM(Frequency) AS Wordcount
                           FROM 
                              WORDxURLxFreq
                           GROUP BY 
                              IDurl;""")
      self.conn.commit()
      print("Table URLxTotalWORDS Populated")

   def CreateTF_IDF(self):
      self.CreateIDxTotalURLS()
      self.CreateURLxTotalWORDS()

      self.DropTable('TFIDF')
      self.cursor.execute("""
         CREATE TABLE TFIDF (
               IDurl UUID NOT NULL,
               IDword UUID NOT NULL,
               tfidf FLOAT NOT NULL,
               PRIMARY KEY (IDurl, IDword),
               FOREIGN KEY (IDurl) REFERENCES IDxURL(ID),
               FOREIGN KEY (IDword) REFERENCES IDxWord(ID)
         );
      """)
      self.conn.commit()
      print("Table TFIDF Created")

      self.cursor.execute("""
         INSERT INTO TFIDF (IDurl, IDword, tfidf)
         SELECT 
               wuf.IDurl,
               wuf.IDword,
               (wuf.Frequency * 1.0 / utw.Wordcount) * LOG((SELECT COUNT(*) FROM urlxtotalwords) * 1.0 / itu.URLcount)
         FROM 
               WORDxURLxFreq wuf
         JOIN 
               URLxTotalWORDS utw ON wuf.IDurl = utw.IDurl
         JOIN 
               IDxTotalURLs itu ON wuf.IDword = itu.IDword;
      """)
      self.conn.commit()
      print("TF-IDF values inserted into TFIDF table")

   ## -------


   def DropTable(self, table_name):
         self.cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
         self.conn.commit()
         print(f"Table {table_name} dropped successfully")

   def initialize_check(self):
      # Read SQL file for creating tables
      with open(os.path.join('dbs/sql_db', 'create_tables.sql'), 'r') as sql_file:
         sql_script = sql_file.read()

      # List of tables to check
      tables_to_check = ['IDxURL', 'IDxWord', 'URLxFreq', 'WORDxURLxFreq']

      # Check if each table exists and has the correct structure
      for table in tables_to_check:
         # Check if the table exists
         self.cursor.execute(f"SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = '{table}'")
         table_exists = self.cursor.fetchone()[0] == 1

         if not table_exists:
               print(f"Table {table} does not exist. Creating...")
               if table == 'IDxURL':
                  self.CreateIDxURLTable()
               elif table == 'IDxWord':
                  self.CreateIDxWordTable()
               elif table == 'URLxFreq':
                  self.CreateURLxFreqTable()
               elif table == 'WORDxURLxFreq':
                  self.CreateWORDxURLxFreqTable()
               self.conn.commit()
         
         self.CreateTF_IDF()

               

   def EmptyTables(self):
      
      self.cursor.execute("DELETE FROM TFIDF")
      self.cursor.execute("DELETE FROM URLxFreq")
      self.cursor.execute("DELETE FROM WORDxURLxFreq")
      self.cursor.execute("DELETE FROM IDxURL")
      self.cursor.execute("DELETE FROM IDxWord")
      self.conn.commit()
      print("Tables emptied successfully")

   def InsertIntoIDxURL(self, URLs):
      for URL in tqdm(URLs, desc="Inserting URLs"):
         id = uuid.uuid4()
         try:
            self.cursor.execute("""
                  INSERT INTO IDxURL (ID, URL)
                  VALUES (%s, %s)
                  ON CONFLICT (URL) DO NOTHING;
            """, (id, URL))
         except Exception as e:
            print(f"Failed Inserting into IDxURL: {e}")
      self.conn.commit()

   def InsertIntoIDxWord(self, words):
      for word in tqdm(words, desc="Inserting words"):
         id = uuid.uuid4()
         self.cursor.execute("""
            INSERT INTO IDxWord (ID, WORD)
            SELECT %s, %s
            WHERE NOT EXISTS (SELECT 1 FROM IDxWord WHERE WORD = %s);
         """, (id, word, word))
      self.conn.commit()

   def InsertIntoURLxFreq(self, URLxFreq, wipe=False):
      '''
      Optimized version of InsertIntoURLxFreq using batch operations.
      '''
      if wipe:
         self.cursor.execute("DELETE FROM URLxFreq")
         self.conn.commit()
      
      urls = list(URLxFreq.keys())
      if not urls:
         return
      
      # Fetch existing URLs in batch
      self.cursor.execute("SELECT URL, ID FROM IDxURL WHERE URL IN %s", (tuple(urls),))
      existing = self.cursor.fetchall()
      existing_dict = dict(existing)
      missing = [url for url in urls if url not in existing_dict]
      
      # Batch insert missing URLs and retrieve their IDs
      if missing:
         # Use execute_values to insert missing URLs and return their IDs
         query = "INSERT INTO IDxURL (URL) VALUES %s RETURNING URL, ID"
         new_urls = [(url,) for url in missing]
         new_records = execute_values(
            self.cursor, query, new_urls, fetch=True
         )
         existing_dict.update(dict(new_records))
    
      # Prepare ID-frequency pairs
      id_freq_pairs = [(existing_dict[url], freq) for url, freq in URLxFreq.items()]
      
      # Batch upsert into URLxFreq
      execute_values(
         self.cursor,
         """INSERT INTO URLxFreq (IDurl, Freq) VALUES %s
            ON CONFLICT (IDurl) DO UPDATE SET
            Freq = URLxFreq.Freq + EXCLUDED.Freq""",
         id_freq_pairs,
         page_size=500  # Tune based on performance
      )
      self.conn.commit()

   def InsertIntoWORDxURLxFreq(self,url, WORDxFreq):
      id = self.cursor.execute("SELECT ID FROM IDxURL WHERE URL = %s", (url,))
      id = self.cursor.fetchone()
      if id is None:
         print(f"URL {url} has not yet been added to DB")
         print(f"Adding URL {url} to DB ...")
         self.InsertIntoIDxURL([url])
         id = self.cursor.execute("SELECT ID FROM IDxURL WHERE URL = %s", (url,))
         id = self.cursor.fetchone()
      id = id[0]

      for word, freq in tqdm(WORDxFreq.values, desc="Inserting WORDxFreq"):
         word_id = self.cursor.execute("SELECT ID FROM IDxWord WHERE WORD = %s", (word,))
         word_id = self.cursor.fetchone()
         if word_id is None:
               
               self.InsertIntoIDxWord([word])
               word_id = self.cursor.execute("SELECT ID FROM IDxWord WHERE WORD = %s", (word,))
               word_id= self.cursor.fetchone()
         word_id = word_id[0]
         
         self.cursor.execute("""
            INSERT INTO WORDxURLxFreq (IDurl, IDword, Frequency)
            VALUES (%s, %s, %s)
            ON CONFLICT (IDurl, IDword) DO UPDATE
            SET Frequency = EXCLUDED.Frequency;
         """, (id, word_id, freq))
      self.conn.commit()


   def QueryTFIDF(self, word):
      word_id = self.cursor.execute("SELECT ID FROM IDxWord WHERE WORD = %s", (word,))
      word_id= self.cursor.fetchone()
      if word_id is None:
         print(f"Word {word} has not yet been added to DB")
         return []

      word_id = word_id[0]
      self.cursor.execute("""
         SELECT 
               IDurl,
               tfidf
         FROM 
               TFIDF
         WHERE 
               IDword = %s
         ORDER BY 
               tfidf DESC;
      """, (word_id,))

      results = self.cursor.fetchall()

      # for res in results:
      #     url = self.cursor.execute("SELECT URL FROM IDxURL WHERE ID = %s", res[0]).fetchone()
      #     res[0] = url[0]

         # print(f"URL: {res[0]} TF-IDF: {res[1]}")

      
      return results
   



   
   def SentenceTFIDF(self,query):
      query_words = query.split(" ")
      list_results = []
      for word in query_words:

         results = self.QueryTFIDF(word)
         print('done')
         for result in results:
               list_results.append(result)

   
      # print(list_results)


      
      id_counts = Counter(id for id, _ in list_results)

      list_results = [tupl for tupl in list_results if id_counts[tupl[0]] == len(query_words)]
   
      
      final_results = defaultdict(float)
      

      for id, value in list_results:
         final_results[id] += value
      

      
      final_results = dict(sorted(final_results.items(), key=lambda item: item[1], reverse=True))
   
      return list(final_results)[:20]
   

   def sentence_vector_tf_idf(self, query, Top_n=2000):
      '''
      This TF-IDF function calculates the TF-IDF of each word in the query and then calculates
      the TF-IDF of the sentence to generate a sentence vector.
      
      Example:
         query = "hello world"
         Query_vector = [0.5, 0.3]
         
      After building the document vectors, you can perform a cosine similarity with the sentence
      vectors in the database.
      '''
      query_words = query.split()  # Handles extra spaces gracefully

      # Aggregate results in a dictionary: {doc_id: {word: tfidf, ...}}
      df = pd.DataFrame(columns=['ID'])

      for word in query_words:
         results = self.QueryTFIDF(word)
         temp_df = pd.DataFrame(results, columns=['ID', f'{word}'])
         ids = [id for id, _ in results]
         scores = [score for _, score in results]

         temp_df['ID'] = ids
         temp_df[f'{word}'] = scores

         df = pd.merge(df, temp_df, on='ID', how='outer')

      ## Fill NaN values with 0
      df.fillna(0, inplace=True)

      # Extra duplicate check (should not be necessary since keys are unique)
      if df.duplicated(subset='ID').any():
         raise Exception("Duplicates found in ID column")

      # Optionally, save the DataFrame for inspection
      df.to_csv('df.csv', index=False)
      print(df)

      # TODO: Calculate the query vector for cosine similarity

      ## TF part
      query_words = query.split()
      total_words = len(query_words)
      word_counts = Counter(query_words)
      
      query_vector=[]
      
      for word, count in word_counts.items():
         # Compute term frequency (TF)
         tf = count / total_words

         self.cursor.execute("SELECT ID FROM IDxWord WHERE WORD = %s", (word,))
         word_id = self.cursor.fetchone()
         if word_id is None:
               print(f"Word {word} has not yet been added to DB")
               continue

         # Fetch IDF from SQL DB for the current word
         self.cursor.execute("""
            SELECT LOG((SELECT COUNT(*) FROM idxurl) * 1.0 / URLcount) AS idf
            FROM IDxTotalURLs
            WHERE IDword = %s
        """, (word_id,))
        
         result = self.cursor.fetchone()    
         # If the word is not in the database, set IDF to 0 (or use an alternative default)
         idf = float(result[0]) if result is not None else 0

         # Calculate the TF-IDF weight for the word
         print(word)
         query_vector.append(tf * idf)
         


      ## Calculate the query vector for cosine similarity
      # Convert vectors into a format for cosine similarity computation
      query_vector_np = np.array(query_vector)
      doc_vectors = df.drop(columns='ID').to_numpy()

     
      print(query_vector_np)
      # Reshape query_vector_np to be 2D for cosine similarity calculation
      query_vector_np = query_vector_np.reshape(1, -1)

      # Calculate Euclidean distances
      distances = np.linalg.norm(doc_vectors - query_vector_np, axis=1)
      print('distances')
      print(distances)
      print(f'min: {distances.min()}')
      print(f'max: {distances.max()}')
      print(np.argsort(distances))

      most_similar_indices = np.argsort(distances)[:Top_n]  
      ids = df.iloc[most_similar_indices]['ID'].tolist()
      return ids

   def find_url(self, id):
      url = self.cursor.execute("SELECT URL FROM IDxURL WHERE ID = %s", id).fetchone()
      return url[0]

   def DeleteTale(self,TableName):
      self.cursor.execute(f"DROP TABLE {TableName}")
      self.conn.commit()
      print(f"Table {TableName} deleted successfully")


   def CheckIfTableExists(self,TableName):
      self.cursor.execute(f"""IF OBJECT_ID('{TableName}', 'U') IS NOT NULL
                     SELECT 'Table exists'
                     ELSE
                     SELECT 'Table does not exist'""")
      row = self.cursor.fetchone()
      if row[0] == 'Table exists':
         return True
      return False

   def EmptyTable(self,TableName):
      self.cursor.execute(f"DELETE FROM {TableName}")
      self.conn.commit()
      print(f"Table {TableName} emptied successfully")


   def get_all_dbs(self):
      '''
      This function is used to get all the databases available in Postgres
      '''
      # Get all the databases in postgres
      self.cursor.execute("SELECT datname FROM pg_database WHERE datistemplate = false;")
      databases = self.cursor.fetchall()

      databases = [db[0] for db in databases]

      return databases
   
   def fill_IDxFreq(self,mongo_db):
      '''
      This function is used to fill the IDxFreq table with the frequency of each url in the database

      '''

      mongo_db.connect()
      ids = mongo_db.find_all_ids()
      table = mongo_db.get_internal_links(ids=ids)
      self.InsertIntoURLxFreq(table,wipe=True)
      mongo_db.close_connection()

      return table
   
   
   
   