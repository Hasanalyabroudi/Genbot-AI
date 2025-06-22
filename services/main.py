from dbs.mongo_db.db import db as mongo_db
from dbs.sql_db.db import db as sql_db
from text_processing.TextProcessing import TextProcessing
from services.save_in_dbs import save_to_db
import os

from dotenv import load_dotenv
load_dotenv()

MONGO_CONNECTION_STRING = os.getenv('MONGO_CONNECTION_STRING')

SQL_SERVER = os.getenv('SQL_SERVER')
SQL_DATABASE = os.getenv('SQL_DATABASE')
SQL_USERNAME = os.getenv('SQL_USERNAME')  
SQL_PASSWORD = os.getenv('SQL_PASSWORD')
     


TextProcesser = TextProcessing()
mongo_db_ = mongo_db(MONGO_CONNECTION_STRING)
sql_db_ = sql_db(SQL_SERVER,SQL_DATABASE,SQL_USERNAME,SQL_PASSWORD)
saver = save_to_db(sql_db_,mongo_db_,TextProcesser)




