from concurrent.futures import ThreadPoolExecutor
import os
from fastapi import FastAPI
from dbs.mongo_db.db import db as mongo_db
from dbs.sql_db.db import db as sql_db
from dbs.qdrant_db.db import db as qdrant_db
from api import app
from time import sleep
from dotenv import load_dotenv
import asyncio
import subprocess



load_dotenv()




def connect_to_databases(app: FastAPI, db: str = None):
    try:
        mongo_db_ = mongo_db(
        os.getenv('MONGO_CONNECTION_STRING'),
        f'{db}'
        )
      
        sql_db_ = sql_db(
            os.getenv('SQL_SERVER_IP'),
            f'{db}',
            os.getenv('SQL_USERNAME'),
            os.getenv('SQL_PASSWORD')
            
        )
        qdrant_db_ = qdrant_db(
            os.getenv('QDRANT_CONNECTION_STRING'),
            f'{db}'
        )
        
        ## Connect to databases
        sql_db_.connect()
        mongo_db_.connect()
        qdrant_db_.connect()

        ## add to a connection pool
        app.state.connection_pool[db] = {
            'qdrant': qdrant_db_,
            'sql': sql_db_,
            'mongo': mongo_db_
        }

    except Exception as e:
        print("Trying to reestablish the connection...")
        print(e)
        sleep(15)
        connect_to_databases(app, db)



def get_all_dbs():
    '''
    This function returns all the databases available (Not necessarily in the connection pool)

    Steps:
    1. Get all the databases in postgres
    2. Get all the databases in mongo
    3. Get all the databases in qdrant
    4. Return common databases in all three

    Returns:
    json: list of databases 

    example:
    {
        "databases": ["db1", "db2", "db3"]
    }
    
    '''

    ## check if any connection is available in the connection pool
    if app.state.connection_pool:
        ## take last connection and return the databases
        sql_db_ = list(app.state.connection_pool.values())[0]['sql']
        mongo_db_ = list(app.state.connection_pool.values())[0]['mongo']
        qdrant_db_ = list(app.state.connection_pool.values())[0]['qdrant']

        ## check if the connection is still active
        try:
            sql_db_.cursor.execute("SELECT 1")
            mongo_db_.client.server_info()
            qdrant_db_.client.get_version()

            print("All connections are active")
        except:
            # Delete the connection from the connection pool
            del app.state.connection_pool[list(app.state.connection_pool.keys())[0]]
            get_all_dbs()
            

    else:
        ## get all the databases in postgres
        sql_db_ = sql_db(
            os.getenv('SQL_SERVER_IP'),
            'postgres',
            os.getenv('SQL_USERNAME'),
            os.getenv('SQL_PASSWORD')
        )

        sql_db_.connect()


        ## get all the databases in mongo
        mongo_db_ = mongo_db(
            os.getenv('MONGO_CONNECTION_STRING'),
            'test'
        )

        mongo_db_.connect()


        ## get all the databases in qdrant
        qdrant_db_ = qdrant_db(
            os.getenv('QDRANT_CONNECTION_STRING'),
            'admin'
        )

        qdrant_db_.connect()


    postgres_dbs = sql_db_.get_all_dbs()
    mongo_dbs = mongo_db_.get_all_dbs()
    qdrant_dbs = qdrant_db_.get_all_collections()

    print("Qdrant dbs: ", qdrant_dbs)

    ## return common databases in all three
    return {"databases": list(set(postgres_dbs) & set(mongo_dbs) & set(qdrant_dbs))}
