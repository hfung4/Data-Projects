import os
from dotenv import load_dotenv, find_dotenv
from typing import List


# llm
from langchain import LLMMathChain, SQLDatabase

# tools
from langchain.agents import Tool, AgentType, initialize_agent
from langchain.tools import DuckDuckGoSearchRun, PubmedQueryRun
from langchain_experimental.sql import SQLDatabaseChain

from langchain.agents import initialize_agent
from langchain.agents import AgentType

# memory
from langchain.prompts import MessagesPlaceholder
from langchain.memory import ConversationBufferMemory



"""This function outputs a list of tools that could be used by the 
langchain agent
    Args:
       llm : llm endpoint object
    Returns:
        tools(list): list of tools
"""


def get_tools(llm) -> List:
    # Load environment variables to get the db_uri
    _ = load_dotenv(find_dotenv())

    # Load the database from uri, using a langchain method
    db = SQLDatabase.from_uri(os.getenv("DB_URI"))

    # Tools
    ddg_search = DuckDuckGoSearchRun()
    llm_math_chain = LLMMathChain.from_llm(llm)
    pubmed_search = PubmedQueryRun()
    db_chain = SQLDatabaseChain.from_llm(llm,db,verbose=True)


    # List of tools
    tools = [
    Tool(
        name="DDG-Search",
        func = ddg_search.run,
        description= "useful for when you need to answer questions about current events. You should ask targeted questions"    
    ),
    Tool(
        name = "Calculator",
        func=llm_math_chain.run,
        description = "useful for answering questions about math"
    ),
    Tool(
        name = "Pubmed-Search",
        func = pubmed_search.run,
        description = "useful for answer questions about medical research, drugs, clinical trials, and diseases"
    ),
    Tool(
        name="takeda-survey-data",
        func = db_chain.run,
        description= '''Useful for answering questions about the takeda survey data.
        Given an input question, first infer the column name that is of interest, then create a syntactically correct sql query to run. 
        The table is called 'survey_responses' and the query must be compatible with sqlite3.
        If asked about the number of columns in 'survey_responses', use this query: 'select count(*) from pragma_table_info('survey_responses' 
        From the query results, return the answer in at most 3 to 4 sentences.   
        '''
    )]
    return tools


"""This function creates a custom langchain agent
    Args:
        llm: llm endpoint object
        tools (list): a list of tools to be used by the agent
    Returns:
       agent: Custom agent
"""


def create_agent(llm , tools):
    
    # Prompt components
    PREFIX = """Have a conversation with a human, answering the following questions as best you can.
    You have access to the following tools:"""

    FORMAT_INSTRUCTIONS = """Use the following format:
    Question: the input question you must answer
    Thought: you should always think about what to do
    Action: the action to take, should be one of the tools you have access to
    Action Input: the input to the action
    Observation: the result of the action
    ... (this Thought/Action/Action Input/Observation can repeat N times)
    Thought: I now know the final answer
    Final Answer: the final answer to the original input question"""

    SUFFIX = """Begin!"
    Question: {input}
    Thought:{agent_scratchpad}"""
    
    agent_kwargs = {
    "prefix": PREFIX,
    'format_instructions':FORMAT_INSTRUCTIONS,
    "suffix":SUFFIX,
    "extra_prompt_messages": [MessagesPlaceholder(variable_name="memory")],
    }
    
    memory = ConversationBufferMemory(memory_key="memory", return_messages=True)
    
    agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=True,
    agent_kwargs=agent_kwargs,
    memory=memory,
    handle_parsing_errors="Check your output and make sure it conforms!")
 
    return agent

