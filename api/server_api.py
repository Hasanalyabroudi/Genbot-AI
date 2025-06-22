
import markdown
from pipeline.response import process_and_answer,full_agent_research_response
from api.functions import connect_to_databases,get_all_dbs
from api import app
from fastapi.middleware.cors import CORSMiddleware

import time
import uuid
import asyncio
    
app.add_middleware(
    CORSMiddleware,
    allow_origins='*',  # or use ["*"] for all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

## status
@app.get("/status")
async def status():
    return {"status": "running"}

## get all databases
@app.get("/databases")
async def get_databases():
    return get_all_dbs()

## Response generation endpoint
@app.get("/generate_response/db={db}/query={query}")
async def generate_response_api(query: str,db:str):

    ## check if the db is in the connection pool
    if db not in app.state.connection_pool: 
        connect_to_databases(app, db)

    else:
        ## check if the connection is still active
        try:
            app.state.connection_pool[db]['sql'].cursor.execute("SELECT 1")
            app.state.connection_pool[db]['mongo'].client.server_info()
            app.state.connection_pool[db]['qdrant'].client.get_version()
        except:
            connect_to_databases(app, db)
    
    now = time.time()
    current_time = time.localtime(now)
    hour = current_time.tm_hour
    minute = current_time.tm_min
    second = current_time.tm_sec
    
    requestid = str(uuid.uuid4())
    print(f"Starting request {requestid}...   at {hour}:{minute}:{second}")
    response = full_agent_research_response(query=query,embeddings=app.state.embeddings,qdrant=app.state.connection_pool[db]['qdrant'],ai_agent=app.state.ai_agent)
    # response = process_and_answer(Query=query,qdrant=app.state.connection_pool[db]['qdrant'],sql_db=app.state.connection_pool[db]['sql'],mongo_db=app.state.connection_pool[db]['mongo'],text_cleaner=app.state.text,embeddings=app.state.embeddings)
    print(f"Finished: Time taken for request {requestid}: {time.time()-now} seconds")

    
    ## markdown to html
    response = markdown.markdown(response)


    
    return {"reply": response}

# ## asynch crawl endpoint | User submit a domain to crawl
# @app.post("/crawl")
# async def crawl_domain(domain: str):
#     '''
#     Request body:
#     {
#         "domain": "domain_name"
#     }
    
#     '''

#     ## start the crawl
#     asyncio.create_task(start_crawl(domain))


#     return {"domain": domain, "status": "Crawling started","crawl_id": str(uuid.uuid4())}


