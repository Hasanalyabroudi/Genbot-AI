import pandas as pd
from math import log

class search_engine:

    def __init__(self,mongo_db,sql_db,vector_db,text_cleaner,embdder=None):
        self.mongo_db = mongo_db
        self.sql_db = sql_db
        self.vector_db = vector_db
        self.text_cleaner = text_cleaner
        self.embdder = embdder

    def perform_tf_idf(self,word):
        '''
        This function performs the tf-idf of the word

        This function will:
            TF:
                - Use table WORDxURLxFreq to get the frequency of the word all the urls
                - Use URLxTotalWords to get the total number of words in all the urls

            IDF:
                - Use table IDxURL to get the number of urls
                - Use table WORDxURLxFreq to get the number of urls with the word


        All of the above will be performed usign the SQL query

        Args:
            word (str): The word to perform the tf-idf

        Returns:    
            pd.DataFrame: A dataframe with the following columns:
                - URL: The url
                - TF: The term frequency of the word in the url
                - IDF: The inverse document frequency of the word
                - TF-IDF: The product of TF and IDF
        '''

        ## Connect to the SQL database
        self.sql_db.connect()


        ## word Id
        self.sql_db.cursor.execute(f"SELECT id FROM IDxWord WHERE word = '{word}'")
        word_id = self.sql_db.conn.fetchone()[0]

        ## total documents
        self.sql_db.cursor.execute("SELECT COUNT(DISTINCT url) FROM IDxURL")
        total_documents = self.sql_db.conn.fetchone()[0]

        ## total documents with the word
        self.sql_db.cursor.execute(f"SELECT COUNT(DISTINCT url) FROM WORDxURLxFreq WHERE word_id = {word_id} AND freq > 0")
        total_documents_with_word = self.sql_db.conn.fetchone()[0]

        ## Calculate the idf
        idf = log(total_documents / total_documents_with_word)

        ## Get the urls with the word
        self.sql_db.cursor.execute(f"SELECT url,freq FROM WORDxURLxFreq WHERE word_id = {word_id}")   

        ## total words in the url
        self.sql_db.cursor.execute(f"SELECT url,total_words FROM URLxTotalWords")
        total_words = dict(self.sql_db.cnon.fetchall())


        ## Calculate the tf-idf
        data = []
        for url,freq in self.sql_db.conn.fetchall():
            tf = freq / total_words[url]
            tf_idf = tf * idf
            data.append([url,tf,idf,tf_idf])

        ## Close the connection
        self.sql_db.CloseConnection()

        return pd.DataFrame(data,columns=['URL','TF','IDF','TF-IDF'])
        

    def perform_tf_idf2(self, word):
        '''
        This function performs the tf-idf calculation using the correct table structure
        '''
        query = """
            WITH word_id AS (
                SELECT ID FROM IDxWord WHERE WORD = %s
            ),
            tf_data AS (
                SELECT 
                    w.IDurl,
                    w.Frequency::float / ut.Wordcount AS TF,
                    ut.Wordcount
                FROM WORDxURLxFreq w
                JOIN URLxTotalWords ut ON w.IDurl = ut.IDurl
                WHERE w.IDword = (SELECT ID FROM word_id)
            ),
            idf_calculation AS (
                SELECT LOG(
                    (SELECT COUNT(ID)::float FROM IDxURL) / 
                    NULLIF((SELECT COUNT(DISTINCT IDurl) FROM WORDxURLxFreq WHERE IDword = (SELECT ID FROM word_id)), 0)
                ) AS IDF
            )
            SELECT 
                u.URL,
                t.TF,
                i.IDF,
                t.TF * i.IDF AS "TF-IDF"
            FROM tf_data t
            CROSS JOIN idf_calculation i
            JOIN IDxURL u ON t.IDurl = u.ID
            ORDER BY "TF-IDF" DESC;
        """
        
        df = pd.read_sql(query, self.sql_db.conn, params=(word,))
        return df
            