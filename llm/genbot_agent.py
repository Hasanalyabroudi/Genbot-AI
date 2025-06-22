import time
from langchain_openai import AzureChatOpenAI
from langchain import hub
from langchain.agents import AgentExecutor, create_tool_calling_agent
from llm.agent_tool_box import *
from langchain_core.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

class ai_agent():
    def __init__(self, openai_key, openai_endpoint, openai_api_version="2025-01-01-preview", azure_deployment="gpt-4o"):
        self.openai_key = openai_key
        self.openai_endpoint = openai_endpoint
        self.openai_api_version = openai_api_version
        self.azure_deployment = azure_deployment

        os.environ["AZURE_OPENAI_API_KEY"] = openai_key
        os.environ["AZURE_OPENAI_ENDPOINT"] = openai_endpoint

        self.llm = AzureChatOpenAI(
            openai_api_version=openai_api_version,
            azure_deployment=azure_deployment,
        )

        self.tools = [add, validate_list]
        # Get the prompt to use - can be replaced with any prompt that includes variables "agent_scratchpad" and "input"!
        self.prompt = hub.pull("hwchase17/openai-tools-agent")
        # Construct the tool calling agent
        self.agent = create_tool_calling_agent(self.llm, self.tools, self.prompt)

        # Create an agent executor by passing in the agent and tools
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=True,
            return_intermediate_steps=True,
            early_stopping_method="force",
            max_iterations=25
        )

    def answer(self, question):
        chat_history = []
        while True:
            # Pass input correctly without extra keys
            descriptions = self.agent_executor.invoke(
                default_prompt(question, chat_history)
            )
            print(descriptions)
            output = descriptions["output"]
            chat_history.append({"input": descriptions["input"], "output": output})
            chat_history = chat_history[-3:]
            print(f"AI: {output}")
            
            # Ask the user if they want to continue
            user_input = input("Do you have another question? (yes/no): ").strip().lower()
            if user_input != "yes":
                break
            
            question = input("Please enter your next question: ").strip()

        return chat_history
    
    def generate_queries(self, question, current_try=0, max_tries=3):
        """
        Generates a unique query that will be used to query the database.
        """
        if current_try > max_tries:
            print("Maximum number of tries reached")
            return [question]
        
        print('Generating queries ...')
        try:
            queries = self.agent_executor.invoke(
                generate_queries_prompt(question)
            )
            str_ = queries['output']
            list_questions = str_.replace("[","").replace("]","").replace('"','').split(",")
            list_questions = list([question.strip() for question in list_questions])
            list_questions = [q for q in list_questions if q.strip()]
            return list(list_questions)
        except Exception as e:
            print(f"Error in generating queries: {e}")
            print("Retrying ...")
            return self.answer_user_question(question, current_try+1, max_tries=max_tries)      
    
    def answer_sub_query(self, query, knowledge_base):
        """
        This function takes a query and returns a response from the LLM using only the provided context.
        """
        try:
            response = self.agent_executor.invoke(
                answer_user_query_prompt(query, knowledge_base)
            )
            return response['output']
        except Exception as e:
            print(f"Error in answering sub query: {e}")
            return None
        
    def final_answer(self, query, knowledge_base):
        """
        This function takes a query and returns a final response from the LLM using only the provided context.
        """
        try:
            response = self.agent_executor.invoke(
                final_answer_prompt(query, knowledge_base)
            )
            return response['output']
        except Exception as e:
            print(f"Error in answering sub query: {e}")
            return None
        
    def copy(self):
        """
        This function returns a copy of the agent.
        """
        return ai_agent(self.openai_key, self.openai_endpoint, self.openai_api_version, self.azure_deployment)


from langchain.schema import HumanMessage
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os 
from dotenv import load_dotenv

load_dotenv()

# Define the API key and endpoint
os.environ["AZURE_OPENAI_API_KEY"] = os.getenv('AZURE_OPENAI_API_KEY_CAPSTONE')
os.environ["AZURE_OPENAI_ENDPOINT"] = 'https://genbotai.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2025-01-01-preview'

# Updated system prompt ensuring the answer is solely based on the provided knowledge base.
system_prompt2 = '''
You are an AI Tutor. Under no circumstances are you allowed to use any information other than what is provided in the given knowledge base. You must answer the user's question exclusively using the provided sources, and you are forbidden from incorporating any external data or making assumptions beyond that.

Your purpose is to provide precise and insightful answers to user queries about their classes and courses using ONLY the information provided below.
Respond only to questions that are directly supported by the provided sources.
Always reply in the language in which the question was asked.
Ensure your responses are clear and readable, with two blank lines between each answer.

If the answer to the question cannot be found within the provided sources, respond exactly with: 
"I'm not quite sure about that. You might want to do a bit more research on this topic."

Do not add, infer, or assume any additional information beyond the given knowledge base.

Here is the user question: {Question}

And here are the sources you'll use to formulate your answer:

Knowledge Base: {Sources}

Chat History: {ChatHistory}
'''

def generate_response(Question, Sources, ChatHistory):
    LLM = AzureChatOpenAI(
        openai_api_version="2024-08-01-preview",
        azure_deployment="gpt-4o",
    )
    
    Prompt = PromptTemplate(  
        input_variables=["Question", "Sources", "ChatHistory"],  
        template=system_prompt2
    ) 
    
    chain = Prompt | LLM | StrOutputParser()
    response = chain.invoke({"Question": Question, "Sources": Sources, "ChatHistory": ChatHistory})
    return response

def generate_final_response(Question, Sources, ChatHistory):
    LLM = AzureChatOpenAI(
        openai_api_version="2024-08-01-preview",
        azure_deployment="gpt-4o",
    )
    
    Prompt = PromptTemplate(  
        input_variables=["Question", "Sources", "ChatHistory"],  
        template=system_prompt2
    ) 
    
    chain = Prompt | LLM | StrOutputParser()
    response = chain.invoke({"Question": Question, "Sources": Sources, "ChatHistory": ChatHistory})
    return response
