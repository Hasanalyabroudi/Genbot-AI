import os
from langchain_openai import AzureOpenAIEmbeddings
from PyPDF2 import PdfReader
from dotenv import load_dotenv

load_dotenv()

AZURE_OPENAI_API_KEY = os.getenv('AZURE_OPENAI_API_KEY_CAPSTONE')
EMBEDDINGS_ENDPOINT = os.getenv('AZURE_OPENAI_ENDPOINT_CAPSTONE')



embeddings =  AzureOpenAIEmbeddings(openai_api_key = AZURE_OPENAI_API_KEY,azure_endpoint=EMBEDDINGS_ENDPOINT,model="text-embedding-3-large")  # Generating embeddings

def CreateEmbedding(Corpus):
    return embeddings.embed_documents(Corpus)


# print(CreateEmbedding("Hello World"))  # Test the function
embeddings = CreateEmbedding(["Hello World"])  # Test the function
print(len(embeddings[0]))  # Test the function