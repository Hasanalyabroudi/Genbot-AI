from langchain_openai import AzureOpenAIEmbeddings
from dbs.sql_db.db import db as sql_db
from dbs.mongo_db.db import db as mongo_db
from dbs.qdrant_db.db import db as qdrant_db
from text_processing.TextProcessing import TextProcessing
from pipeline.response import process_and_answer

import os
from dotenv import load_dotenv
import time
load_dotenv()


## Load environment variables
AZURE_OPENAI_API_KEY = os.getenv('AZURE_OPENAI_API_KEY_CAPSTONE')
EMBEDDINGS_ENDPOINT = os.getenv('AZURE_OPENAI_ENDPOINT_CAPSTONE')

## Azure Embeddings
embedder =  AzureOpenAIEmbeddings(openai_api_key = AZURE_OPENAI_API_KEY,azure_endpoint=EMBEDDINGS_ENDPOINT,model="text-embedding-3-large")  # Generating embeddings


mongo_db_ = mongo_db(
        os.getenv('MONGO_CONNECTION_STRING'),
        'uottawa_db'
    )

## Connect to MongoDB
mongo_db_.connect()

sql_db_ = sql_db(
    os.getenv('SQL_SERVER_IP'),
    'uottawa_db',
    os.getenv('SQL_USERNAME'),
    os.getenv('SQL_PASSWORD')
    
)
## Connect to the SQL database
sql_db_.connect()

qdrant_db_ = qdrant_db(
    'http://localhost:6333',
    'uottawa_db'
)
qdrant_db_.connect()



text = TextProcessing()

print(process_and_answer(Query="what is coop at uottawa?",qdrant=qdrant_db_,sql_db=sql_db_,mongo_db=mongo_db_,text_cleaner=text,embeddings=embedder))



    

