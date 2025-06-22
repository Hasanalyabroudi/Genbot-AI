from langchain_openai import AzureOpenAIEmbeddings
from pipeline.response import process_and_answer,llm_agent_researcher,multi_llm_agent_researcher,full_agent_research_response
import os 
from dbs.mongo_db.db import db as mongo_db
from dbs.sql_db.db import db as sql_db
from dbs.qdrant_db.db import db as qdrant_db
from text_processing.TextProcessing import TextProcessing
from llm.genbot_agent import ai_agent

import os
from dotenv import load_dotenv
import time

load_dotenv()


## Env variables
AZURE_OPENAI_API_KEY = os.getenv('AZURE_OPENAI_API_KEY_CAPSTONE')
EMBEDDINGS_ENDPOINT = "https://genbotai.openai.azure.com/openai/deployments/text-embedding-3-large/embeddings?api-version=2023-05-15"


db = 'www_uottawa_ca_db'

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

embeddings = AzureOpenAIEmbeddings(openai_api_key = AZURE_OPENAI_API_KEY,azure_endpoint=EMBEDDINGS_ENDPOINT,model="text-embedding-3-large")  # Generating embeddings
text = TextProcessing()


print(full_agent_research_response(query='what are the first year courses in software engineering?',qdrant=qdrant_db_,embeddings=embeddings,ai_agent=ai_agent_))


# start_time = time.time()
# queries = [
#     "What is software engineering?",
#     "What is computer science?",
#     "What is financial engineering?",
# ]
# response = (multi_llm_agent_researcher(queries=queries,embeddings=embeddings,qdrant=qdrant_db_))

# for query, answer in zip(queries, response):
#     print(f"Query: {query}")
#     print(f"Answer: {answer}")

# end_time = time.time()
# total_time = end_time - start_time
# print(f"Total time taken: {total_time} seconds")


# URLxFreq = {
#     'https://www.uottawa.ca/study/undergraduate-studies':1,
#     'https://www.uottawa.ca/study/graduate-studies':1


# }
# sql_db_.fill_IDxFreq(mongo_db=mongo_db_)
