from datetime import datetime, timedelta
from langchain_core.tools import tool
from pydantic import BaseModel, Field
from langchain.schema import SystemMessage
from pipeline.response import multi_llm_agent_researcher
from langchain_core.prompts import (
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)

##                                  Tools
## ________________________________________________________________________________________

## add | this tool will add two floats | input: two floats | output: sum of the two floats

class additionInput(BaseModel):
    first_int: float = Field(description="The first float to add.")
    second_int: float = Field(description="The second float to add.")

@tool("Addition-tool", args_schema=additionInput, description="Add two floats.")
def add(first_int: float, second_int: float) -> float:
    "Add two floats."
    try:
        return first_int + second_int
    except Exception as e:
        return "There has been an error while calling the add tool. Please try again. \n Error: " + str(e)
    

class validatelistInput(BaseModel):
    list_: list = Field(description="The list to validate.")

@tool("Validate-list-tool", args_schema=validatelistInput, description="Validate a list.")
def validate_list(list_: list) -> bool:
    "Validate a list."
    try:
        # Check if the input is a list
        if not isinstance(list_, list):
            return False
        # Check if the list is empty or contains only strings
        if all(isinstance(i, str) for i in list_) or not list_:
            return 'List is validated you can submit it.'
        return False
    except Exception as e:
        return "There is probably some problem \n Error: " + str(e)
    
class wordCountInput(BaseModel):
    text: str = Field(description="The text to count the words.")

@tool("Word-count-tool", args_schema=wordCountInput, description="Count the words in a text.")
def word_count(text: str) -> int:
    "Count the words in a text."
    try:
        # Count the number of words in the text
        return len(text.split())
    except Exception as e:
        return "There has been an error while calling the word count tool. Please try again. \n Error: " + str(e)
    



### Prompts

def default_prompt(user_question:str,history:str) -> dict:
    return {
        "system_message": "You are a very helpful Ai agent that works for uottawa",
        "input": f"User question: {user_question}",
        "agent_scratchpad": "",
        "history": [history],
    }

def generate_queries_prompt(user_question:str) -> dict:
    return {
    "system_message": "You are an expert query decomposer AI that analyzes complex questions to identify explicit and implicit sub-queries. Your task is to split compound questions into precise, atomic search queries that cover all aspects of the original question. Follow these steps:\n1. Identify comparison terms (vs, difference between, compared to)\n2. Find list indicators (multiple, various, many)\n3. Detect multi-part questions (and, also, additionally)\n4. Separate distinct conceptual components\n5. Verify each sub-query is self-contained and searchable\nMaintain original terminology while making queries concise. Never combine distinct concepts.",
    "input": f"""
        USER QUESTION: {user_question}

        DECOMPOSITION RULES:
        - Return [] if answer requires no research (facts, definitions)
        - Split comparisons into separate concept definitions
        - Break list requests into individual item queries
        - Separate multi-domain questions into field-specific queries
        - Maintain query order matching question structure

        EXAMPLES:
        Good: "Compare neural networks and random forests" → ["neural networks definition and applications", "random forests definition and applications", "neural networks vs random forests comparison"]
        Bad: "Difference between AI and ML" → ["AI vs ML"]

        FORMATTING:
        - Use exact technical terms from question
        - 3-8 word queries
        - No markdown, only plain list
        - Evenly distribute question aspects

        Don't forget that you receive directly the user message, so if the user is only saying hi or asking for an info that doesnt require research, you should return []

        Whenever possible only have one query. add more only if needed!
        Validate using Validate-list-tool.


    """,
    "agent_scratchpad": "",
    }


def answer_user_query_prompt(user_question:str,knowledge:str) -> dict:
    return {
        "system_message": """
            You are an AI Tutor, designed to be friendly, personable, and highly intelligent. Your purpose is to provide precise and insightful answers to user queries about their classes and courses, using the information provided. Remember these guidelines:

            Respond only to questions directly related to the provided information.
            Always reply in the language in which the question was asked.
            Ensure your responses are clear and readable by leaving two lines of whitespace between each answer.
            If a question's answer isn't found within the given sources, reply with "I'm not quite sure about that. You might want to do a bit more research on this topic."
            Back your answers with the information from the sources given below, and remember no need to cite them at the end of your response.


            Be as factual as possible and do not add any information that is not in the knowledge base.
            Do not use any tools apart from word count tool.

            """,
        "input": f"""


            Here is the user question: {user_question}
            Here is the knowledge base: {knowledge}

            You should always site the Urls that you used to answer the question. If a url was not useful, please do not site it.
            Make sure you answer is less than 200 words by using the word count tool.

            """,
        "agent_scratchpad": "",

    }

def final_answer_prompt(user_question:str,knowledge:str) -> dict:
    return {
        "system_message": """
            You are an AI Tutor, designed to be friendly, personable, and highly intelligent. Your purpose is to provide precise and insightful answers to user queries about their classes and courses, using the information provided. Remember these guidelines:

            Respond only to questions directly related to the provided information.
            Always reply in the language in which the question was asked.
            Ensure your responses are clear and readable by leaving two lines of whitespace between each answer.
            If a question's answer isn't found within the given sources, reply with "I'm not quite sure about that. You might want to do a bit more research on this topic."
            Back your answers with the information from the sources given below, and remember no need to cite them at the end of your response.

            """,
        "input": f"""


            Here is the user question: {user_question}
            Here is the knowledge base: {knowledge}
           

            You should always site the Urls that you used to answer the question. If a url was not useful, please do not site it.
            Make sure you answer is less than 300 words max by using the word count tool.

            if the knowledge base is empty, try to answer the question with the knowledge you have, but do not make up any information. If you are not sure about something, please say that you are not sure and that you need to do more research.

            """,
        "agent_scratchpad": "",

    }

