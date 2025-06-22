from search_engine.SearchEngine import search_engine
from dbs.mongo_db.db import db as mongo_db
from dbs.sql_db.db import db as sql_db

from text_processing.TextProcessing import TextProcessing

import os
from dotenv import load_dotenv
import time
load_dotenv()

mongo_db_ = mongo_db(
        os.getenv('MONGO_CONNECTION_STRING'),
        'Uottawa_db'
    )

sql_db_ = sql_db(
    os.getenv('SQL_SERVER_IP'),
    'uottawa_db',
    os.getenv('SQL_USERNAME'),
    os.getenv('SQL_PASSWORD')
    
)


## Connect to the SQL database
sql_db_.connect()

search_engine_ = search_engine(
    mongo_db_,
    sql_db_,
    None,
    TextProcessing()
)   



start_time = time.time()
df = search_engine_.perform_tf_idf2('eat')
end_time = time.time()

print(f"Query time: {end_time - start_time} seconds")

print(df)

while True:
    try:
        query = input("Enter a query: ")
        start_time = time.time()
        df = search_engine_.perform_tf_idf2(query)
        end_time = time.time()

        print(f"Query time: {end_time - start_time} seconds")

        for i in range(10):
            print(df.iloc[i]['url'],df.iloc[i]['TF-IDF'])

    except Exception as e:
        print(e)
        continue    
            



