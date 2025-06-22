from contextlib import asynccontextmanager
from fastapi import FastAPI
from langchain_openai import AzureOpenAIEmbeddings
from llm.genbot_agent import ai_agent
from text_processing.TextProcessing import TextProcessing
import os
from dotenv import load_dotenv

load_dotenv()


## Env variables
AZURE_OPENAI_API_KEY = os.getenv('AZURE_OPENAI_API_KEY_CAPSTONE')
EMBEDDINGS_ENDPOINT = "https://genbotai.openai.azure.com/openai/deployments/text-embedding-3-large/embeddings?api-version=2023-05-15"


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Connect to the databases
    app.state.connection_pool = {}
    app.state.embeddings =   AzureOpenAIEmbeddings(openai_api_key = AZURE_OPENAI_API_KEY,azure_endpoint=EMBEDDINGS_ENDPOINT,model="text-embedding-3-large")  # Generating embeddings
    app.state.text = TextProcessing()
    app.state.ai_agent = ai_agent(openai_key=AZURE_OPENAI_API_KEY,openai_endpoint='https://genbotai.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2025-01-01-preview')

    yield
    # Close the databases
    app.state.db.close_connection()
    app.state.SQL_db.close_connection()
    print("Databases closed")

app = FastAPI(lifespan=lifespan)

