import uuid
from dbs.db_____ import DBHandler
import os
from dotenv import load_dotenv
import pandas as pd
from TF_IDF_db import SQL_DBHandler
from tqdm import tqdm

SQL_DATABASE = os.getenv('SQL_DATABASE')
SQL_USERNAME = os.getenv('SQL_USERNAME')  
SQL_PASSWORD = os.getenv('SQL_PASSWORD')


DB_URL = os.getenv('DB_URL')
DB_KEY = os.getenv('DB_KEY')
DB_NAME = os.getenv('DB_NAME')




def ConnectToDBs():
    db  = DBHandler(DB_URL, DB_KEY,DB_NAME, DB_NAME) 
    SQL_db = SQL_DBHandler(SQL_DATABASE,SQL_USERNAME)
    SQL_db.ConnectToAzureSQL(SQL_PASSWORD)
    return db, SQL_db

def Build_IDxURL():
    db,SQL_db = ConnectToDBs()
    print('Connected to DB')
    df = pd.DataFrame(columns=['URL'])
    URL = db.QueryDocumentsCustom(elements=['internal_links'])

    # print(len(URL))
    # print(len(URL[0]))
    # print(URL[0])

    print('Building DataFrame ...')


  
    # internal_links = []  
    
    # for i in tqdm(range(len(URL))):  
    #     try:  
    #         for k in range(len(URL[i]['internal_links'])):  
    #             internal_links.append(URL[i]['internal_links'][k])  
    #     except Exception as e:  
    #         print('Error:', e)  
    #         print(URL[i])  
  
    # df = pd.DataFrame(internal_links, columns=['URL'])  
        
    
    # df = df.drop_duplicates(subset=['URL'])
    # print(df)
    # df.to_csv('IDxURL.csv',index=False)

    df = pd.read_csv('IDxURL.csv')

    SQL_db.cursor.execute(f"""SELECT url FROM IDxURL""") # get all urls from db
    db_url = SQL_db.cursor.fetchall()
    db_url = [url[0] for url in db_url]

    print('New URLs')

    urls = df['URL'].tolist()

    urls = [url for url in urls if url not in db_url]
    print('filtered URLs')

    URLxID = pd.DataFrame(columns=['ID','URL'])
    URLxID['URL'] = urls
    URLxID['ID'] = [str(uuid.uuid4()) for i in range(len(urls))]
    print(URLxID.head())
    print('Inserting in SQL')
    SQL_db.InsertIntoIDxURL(URLxID)


def ComputeLinkScore():
    db,SQL_db = ConnectToDBs()
    print('Connected to DB')
    SQL_db.cursor.execute(f"""SELECT URL , ID FROM IDxURL""")
    UniqueLinks = SQL_db.cursor.fetchall()
    UniqueLinks = [url for url in UniqueLinks]

    print('Unique Links')
    # LinkedURL = []
    # for i in tqdm(range(len(URL))):  
    #     try:  
    #         for k in range(len(URL[i]['internal_links'])):  
    #             LinkedURL.append(URL[i]['internal_links'][k])  
    #     except Exception as e:  
    #         print('Error:', e)  
    #         print(URL[i])  

    # print('Building DataFrame ...')
    # LinkedURL = pd.DataFrame(LinkedURL, columns=['URL'])
    # LinkedURL.to_csv('LinkedURL.csv',index=False)
    LinkedURL = pd.read_csv('LinkedURL.csv')
    LinkedURL = LinkedURL['URL'].tolist()

    IDxLinkedCount = pd.DataFrame(columns=['ID','count'])

    for i in tqdm(range(len(UniqueLinks))):
        count = LinkedURL.count(UniqueLinks[i][0])
        IDxLinkedCount.loc[i] = [UniqueLinks[i][1], count]
        # print(f"URL: {UniqueLinks[i]} | Count: {count}")

    print('Inserting in SQL')
    print(IDxLinkedCount.head())
    SQL_db.InsertIntoIDxLinked(IDxLinkedCount)

    Table = pd.DataFrame(Table)
    print('Inserted in SQL')

    

def Build_IDxLinks():
    db,SQL_db = ConnectToDBs()
    print('Connected to DB')
    Table = db.QueryDocumentsCustom(elements=['number_of_links'])
    Table = pd.DataFrame(Table)
    SQL_db.InsertDataFrameInTable('IDxLinks',Table)
    print('Inserted in SQL')

ComputeLinkScore()



