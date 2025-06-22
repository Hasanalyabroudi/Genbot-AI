from llm.genbot_agent import ai_agent
import os 
from dotenv import load_dotenv

load_dotenv()
# Define the api key
key =  os.getenv('AZURE_OPENAI_API_KEY_CAPSTONE')
endpoint ='https://genbotai.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2025-01-01-preview'


ai_agent_ = ai_agent(openai_key=key,openai_endpoint=endpoint)
ai_agent_.answer("What is 2+2")