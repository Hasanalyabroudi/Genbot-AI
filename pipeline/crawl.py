import concurrent

from langchain_openai import AzureOpenAIEmbeddings
from crawler.Crawler import Crawler
from dbs.mongo_db.db import db as mongo_db
from dbs.sql_db.db import db as sql_db
from services.save_in_dbs import save_to_db
from text_processing.TextProcessing import TextProcessing
from url.url import url
from embeddings.embedder import embedder
from dbs.qdrant_db.db import db as qdrant_db
from database_logger.dblogg import dblogg
import argparse

import os 
from dotenv import load_dotenv
load_dotenv()


## get parameters passed with in the command line
parser = argparse.ArgumentParser(description='Crawl a website')
parser.add_argument('--url', type=str, help='URL to crawl', required=True)
args = parser.parse_args()
print(f'URL to crawl: {args.url}')
## cmd format: python -m pipeline.crawl --url "https://qdrant.tech/"


crawler = Crawler()
crawler.set_starting_url(args.url)
dbs_name = crawler.get_domaine_name(crawler.get_urls()[0]).replace('.','_')

logs = sql_db(
        SERVER_IP=os.getenv('SQL_SERVER_IP'),
        DATABASE_NAME='genbot_logs',
        username=os.getenv('SQL_USERNAME'),
        password=os.getenv('SQL_PASSWORD'),
     
    )

dblogg_ = dblogg(
    sql_db= logs
)
db_id = dblogg_.setup_new_db(crawler.get_domaine_name(crawler.get_urls()[0]))
print("dbs name: ",dbs_name)
def logg_progress():

    mongo_db_ = mongo_db(
        os.getenv('MONGO_CONNECTION_STRING'),
        f'{dbs_name}_db'
    )

    mongo_db_.connect()
    total_urls = mongo_db_.find_number_of_documents()
    print(f"Total urls: {total_urls}")
    dblogg_.update_number_of_pages(db_id,total_urls)
    mongo_db_.close_connection()


def save_to_dbs(url):

    mongo_db_ = mongo_db(
        os.getenv('MONGO_CONNECTION_STRING'),
        f'{dbs_name}_db'
    )

    sql_db_ = sql_db(
        os.getenv('SQL_SERVER_IP'),
        f'{dbs_name}_db',
        os.getenv('SQL_USERNAME'),
        os.getenv('SQL_PASSWORD')
     
    )
    qdrant_db_ = qdrant_db(
        os.getenv('QDRANT_CONNECTION_STRING'),
        f'{dbs_name}_db'
    )


    embedder_ = embedder(mongo_db_,qdrant_db_,AzureOpenAIEmbeddings(openai_api_key = os.getenv('AZURE_OPENAI_API_KEY_CAPSTONE'),azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT_CAPSTONE'),model="text-embedding-3-large"))
    TextProcesser = TextProcessing()
    saver = save_to_db(sql_db_, mongo_db_,embedder_, TextProcesser) 
    saver.save_to_dbs(url)
    

mult = 50
print(f"Starting crawler with {mult} threads")

while crawler.to_visit:

    print(f"To visit: {len(crawler.to_visit)} | Visited: {len(crawler.visited)}")

    urls = []
    for i in range(min(mult,len(crawler.to_visit))):
        urls.append(crawler.to_visit.pop(0))

    ## log progress
    logg_progress()

    
    with concurrent.futures.ThreadPoolExecutor(max_workers=mult) as executor:
        # Stage 1: Fetch data
        future_to_url = {executor.submit(url, u): u for u in urls}
        total_urls = []
        response_error = []
        for future in concurrent.futures.as_completed(future_to_url):
            url_ = future_to_url[future]
            try:
                data = future.result()
                total_urls.append(data)
            except Exception as exc:
                print(f"Error: {url_} generated an exception: {exc}")
                response_error.append(url_)

        print('-----------------------------------------------')
        # Update crawler
        for url_ in total_urls:
            crawler.add_urls(url_.internal_links)
            crawler.add_to_visited(url_.url)

        # Stage 2: Save data
        
        future_save_to_dbs = {executor.submit(save_to_dbs, url_): url_ for url_ in total_urls}
        for future in concurrent.futures.as_completed(future_save_to_dbs):
            save_ = future_save_to_dbs[future]
            try:
                data = future.result()  # Ensure no exceptions occurred
                print(f"Saved {save_.url}")
            except Exception as exc:
                print(f"Failed to save {save_.url}: {exc}")
            else:
                print(f"Saved {save_.url}")


        print('-----------------------------------------------')

    
## get all pages from mongo db and save them to sql db
mongo_db_ = mongo_db(
        os.getenv('MONGO_CONNECTION_STRING'),
        f'{dbs_name}_db'
    )

