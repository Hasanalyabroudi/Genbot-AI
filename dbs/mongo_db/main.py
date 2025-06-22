from dbs.mongo_db.db import db
from pymongo import MongoClient
import os 
from dotenv import load_dotenv

load_dotenv()

username = os.getenv("MONGO_DB_PASSWORD")
password = os.getenv("MONGO_DB_USERNAME")

connectionstring = os.getenv("MONGO_CONNECTION_STRING")
print(connectionstring)

mongo_db = db(connectionstring, 'Uottawa_')
mongo_db.connect()


# mongo_db.add_element('embeddings', '0000002')
# mongo_db.update_element('0000001')
