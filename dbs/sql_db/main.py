
from collections import defaultdict
from collections import Counter
import pandas as pd
from dbs.sql_db.db import db
from dotenv import load_dotenv
import os
import time
from dbs.mongo_db.db import db as mongo_db

load_dotenv()


SQL_SERVER_IP = os.getenv('SQL_SERVER_IP')
SQL_DATABASE = 'www_uottawa_ca_db'
SQL_USERNAME = os.getenv('SQL_USERNAME')  
SQL_PASSWORD = os.getenv('SQL_PASSWORD')


print(SQL_SERVER_IP,SQL_DATABASE,SQL_USERNAME,SQL_PASSWORD)

## connect to mongo
mongo_db_ = mongo_db(
    os.getenv('MONGO_CONNECTION_STRING'),
    SQL_DATABASE
)
mongo_db_.connect()


sql_db = db(SQL_SERVER_IP,SQL_DATABASE,SQL_USERNAME,SQL_PASSWORD)
sql_db.connect()
sql_db.CreateTF_IDF()

while True:
    query = input("Enter your query: ")

    start_time = time.time()
    ids = (sql_db.SentenceTFIDF(query))
    end_time = time.time()
    print(ids)
    print(f"Execution time: {end_time - start_time} seconds")

    for id in ids:
        ## Find the url of the document 
        sql_db.cursor.execute("SELECT url FROM idxurl WHERE ID = %s", (id,))
        url = sql_db.cursor.fetchone()
        print(url[0])


## find the url of the documents


# sql_db.initialize_check()
# sql_db.EmptyTables()


# sql_db.CreateTF_IDF()
# results = (sql_db.QueryTFIDF('mechanical'))
# df = pd.DataFrame( columns=['ID', 'TF-IDF'])
# for res in results:
#     df.loc[len(df)] = [res[0], res[1]]


# df.to_csv('mechanical.csv', index=False)






# print(sql_db.QueryTFIDF('software'))

# print(sql_db.SentenceTFIDF("software engineer uottawa"))