import time
import concurrent
from langchain_openai import AzureOpenAIEmbeddings
from dbs.mongo_db.db import db as mongo_db
from dbs.qdrant_db.db import db as qdrant_db
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import os
from dotenv import load_dotenv
load_dotenv()

## Load environment variables
AZURE_OPENAI_API_KEY = os.getenv('AZURE_OPENAI_API_KEY_CAPSTONE')
EMBEDDINGS_ENDPOINT = os.getenv('AZURE_OPENAI_ENDPOINT_CAPSTONE')

## Connect to MongoDB
mongo_db_ = mongo_db(
    os.getenv('MONGO_CONNECTION_STRING'),
    'www_uottawa_ca_db'
)
mongo_db_.connect()

## Connect to Qdrant
qdrant_db_ = qdrant_db(
    os.getenv('QDRANT_CONNECTION_STRING'),
    'www_uottawa_ca_db'
)
qdrant_db_.connect()


## Create Azure Embeddings

embedder =  AzureOpenAIEmbeddings(openai_api_key = AZURE_OPENAI_API_KEY,azure_endpoint=EMBEDDINGS_ENDPOINT,model="text-embedding-3-large")  # Generating embeddings

## Get Total number of documents
ids = mongo_db_.find_all_ids()

print(f"Total number of documents: {len(ids)}")

## loop jump
jump = 25

for i in (range(0, len(ids), jump)):
    try:

        print(f"Indexing {i} to {i+jump}")
        document = [mongo_db_.query_document_by_id(id) for id in ids[i:i+jump]]
        corpus = [doc['original_content'].replace('\n',' ').replace('  ',' ') for doc in document]

        # ## use multithreading to generate embeddings
        # with concurrent.futures.ThreadPoolExecutor(max_workers=jump) as executor:
        #     future_embeddinds = {executor.submit(embedder.embed_documents,c): c for c in corpus}
        #     embeddings = []
        #     for future in concurrent.futures.as_completed(future_embeddinds):
        #         vector = future_embeddinds[future]
        #         try:
        #             data = future.result()
        #             embeddings.append(data[0])
        #         except Exception as exc:
        #             print(f'Error: {exc}')
        #             break

        embeddings = embedder.embed_documents(corpus)

        ## check if embeddings were generated correctly
        if len(embeddings) != len(corpus):
            print("Error in embeddings")
            print(len(embeddings))
            break
        
        if len(embeddings[0])<750:
            print("Error in embeddings")
            print(embeddings[0])
            break

        ## Add embeddings to the database
        for k in range(len(embeddings)):
            qdrant_db_.add_vector(embeddings[k])
            qdrant_db_.add_element_to_payload('id',ids[i+k])
            qdrant_db_.add_element_to_payload('url',document[k]['url'])
            qdrant_db_.add_element_to_payload('id2',document[k]['_id'])
            qdrant_db_.push_to_db()


    except Exception as e:

        if '429' in str(e):
            print("Rate limit exceeded")
            time.sleep(60)
            continue

        print(f"Error: {e}")
        break


