from langchain.schema import HumanMessage
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os 
from dotenv import load_dotenv

load_dotenv()
# Define the api key
os.environ["AZURE_OPENAI_API_KEY"] =  os.getenv('AZURE_OPENAI_API_KEY_CAPSTONE')
os.environ["AZURE_OPENAI_ENDPOINT"] = 'https://genbotai.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2025-01-01-preview'

system_prompt = '''
   You are an AI Tutor, designed to be friendly, personable, and highly intelligent. Your purpose is to provide precise and insightful answers to user queries about their classes and courses, using the information provided. Remember these guidelines:

    Respond only to questions directly related to the provided information.
    Always reply in the language in which the question was asked.
    Ensure your responses are clear and readable by leaving two lines of whitespace between each answer.
    If a question's answer isn't found within the given sources, reply with "I'm not quite sure about that. You might want to do a bit more research on this topic."
    Back your answers with the information from the sources given below, and remember no need to cite them at the end of your response.

    Now, here's the question you're tasked to answer:

    Question: {Question}

    And here are the sources you'll use to formulate your answer:

    Sources: {Sources}

    '''

system_prompt2 = '''
    You are an AI Tutor, designed to be friendly, personable, and highly intelligent. Your purpose is to provide precise and insightful answers to user queries about their classes and courses, using the information provided. Remember these guidelines:

    Respond only to questions directly related to the provided information.
    Always reply in the language in which the question was asked.
    Ensure your responses are clear and readable by leaving two lines of whitespace between each answer.
    If a question's answer isn't found within the given sources, reply with "I'm not quite sure about that. You might want to do a bit more research on this topic."
    Back your answers with the information from the sources given below, and remember no need to cite them at the end of your response.


    Be as factual as possible and do not add any information that is not in the knowledge base.
    Do not use any tools apart from word count tool.

    Here is the user question: {Question}

    And here are the sources you'll use to formulate your answer:

    Here is the knowledge base: {Sources}

    notes:
      You should always site the Urls that you used to answer the question. If a url was not useful, please do not site it.
      Make sure you answer is less than 200 words.
      always make sure to include the sources that you used to answer the question.

    '''



def generate_response(Question,Sources,ChatHistory):

    LLM = AzureChatOpenAI(
    openai_api_version="2024-08-01-preview",
    azure_deployment="gpt-4o",
    )

    Prompt = PromptTemplate(  
    input_variables=["Question","Sources","ChatHistory"],  
    template=system_prompt2
    ) 
    
    chain = Prompt | LLM | StrOutputParser()

    # response = chain.invoke(Question = Question,Sources=Sources,ChatHistory=ChatHistory)
    response = chain.invoke({"Question":Question,"Sources":Sources,"ChatHistory":ChatHistory})
    
    return response

def generate_final_response(Question,Sources,ChatHistory):
    LLM = AzureChatOpenAI(
    openai_api_version="2024-08-01-preview",
    azure_deployment="gpt-4o",
    )
    
    Prompt = PromptTemplate(  
    input_variables=["Question","Sources","ChatHistory"],  
    template=system_prompt2
    ) 
    
    chain = Prompt | LLM | StrOutputParser()

    # response = chain.invoke(Question = Question,Sources=Sources,ChatHistory=ChatHistory)
    response = chain.invoke({"Question":Question,"Sources":Sources,"ChatHistory":ChatHistory})
    
    return response



