import time
from langchain_openai import AzureChatOpenAI
from langchain import hub
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.tools import tool
import os


import os 
from dotenv import load_dotenv

load_dotenv()
# Define the api key
os.environ["AZURE_OPENAI_API_KEY"] =  os.getenv('AZURE_OPENAI_API_KEY_CAPSTONE')
os.environ["AZURE_OPENAI_ENDPOINT"] = os.getenv('AZURE_OPENAI_ENDPOINT_CAPSTONE')
'https://genbotai.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2025-01-01-preview'


@tool
def add(first_int: int, second_int: int) -> int:
    "Add two integers."
    return first_int + second_int


@tool
def exponentiate(base: int, exponent: int) -> int:
    "Exponentiate the base to the exponent power."
    return base**exponent

@tool
def multiply(first_int: int, second_int: int) -> int:
    """Multiply two integers together."""
    return first_int * second_int

@tool
def google_search(query: str) -> str:
    """Search Google for the query."""
    time.sleep(1)
    return f"Here are the search results for '{query}': vlad"


tools = [multiply, add, exponentiate, google_search]


llm = AzureChatOpenAI(
    openai_api_version="2024-08-01-preview",
    azure_deployment="gpt-4o",
)


# Get the prompt to use - can be replaced with any prompt that includes variables "agent_scratchpad" and "input"!
prompt = hub.pull("hwchase17/openai-tools-agent")
prompt.pretty_print()

# Construct the tool calling agent
agent = create_tool_calling_agent(llm, tools, prompt)

# Create an agent executor by passing in the agent and tools
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

start_time = time.time()

result = agent_executor.invoke(
    {
        "input": "difference between software engineer and data scientist at uottawa",
    }
)

end_time = time.time()
total_time = end_time - start_time

print(result)
print(f"Total time taken: {total_time} seconds")


