import os
from dotenv import load_dotenv, find_dotenv
from langchain.callbacks import StreamlitCallbackHandler
from langchain import OpenAI
from langchain.chat_models import ChatOpenAI



# config
from src.config import question_list
# utils
from src.utils import get_tools, create_agent


# streamlit
import streamlit as st


# Load environment variables
_= load_dotenv(find_dotenv())



# Front End --------------------------------------------------------------------------------

# Set page title
st.set_page_config(page_title="The Behaviourial Science Guru", page_icon="🤖", layout="wide")


# Inject custom CSS to set the width of the sidebar
st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            width: 1000px !important; # Set the width to your desired value
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# Sidebar
with st.sidebar:

    st.sidebar.title("The Behavioural Science Guru")
    
    st.markdown('#')

    # Enter the API Key
    API_KEY = st.sidebar.text_input('Enter your OpenAI API Key', type='password')
    if not API_KEY.startswith("sk-"):
        st.warning('Please enter your OpenAI API key!', icon='⚠')
        
    # Custom query
    CUSTOM_QUERY = st.checkbox(label="Enter your own query", 
                        key="Enter your own query", 
                        value = False)
       
    
    # query text dropdown menu, defaults to None
    query = st.selectbox('Some common queries:', 
                         options = question_list, 
                         disabled=((not API_KEY.startswith("sk-")) or CUSTOM_QUERY))
    
    submitted = st.button("Submit Query", type="primary",  disabled=((not API_KEY.startswith("sk-")) or CUSTOM_QUERY))
    
    st.write('#')
    st.write('#')
    CLEAR_HISTORY = st.button("Clear chat history and memory", disabled=((st.session_state.get("agent") is None) or (st.session_state.get("messages") is None)))
    

# App Logic and Main panel --------------------------------------------------------------------------------

if CLEAR_HISTORY:
    st.session_state.pop("agent")
    st.session_state.pop("messages")
    


# Accumulation of messages (i.e. chat history) in a user session ------------------------------
# Init the message history
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role":"assistant","content":"How can I help you today?", "avatar" :"images/hal_9000.png"}  
    ]
     
    
# Display chat messages from history on app rerun (which happens when user asks a new question)
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=message["avatar"]):
        st.write(message["content"])
        

# Create Agent -------------------------------------------------------------------------------- 
if ("agent" not in st.session_state) & (API_KEY.startswith("sk-")):
    llm = ChatOpenAI(temperature=0.0,
                 model="gpt-3.5-turbo-0613", 
                 streaming=True,
                 openai_api_key=API_KEY
                 )
    
    # Get a list of tools to be used by agent
    tools = get_tools(llm)

    # Create agent
    agent = create_agent(llm, tools)
    
    st.session_state["agent"] = agent

        

# App logic
if CUSTOM_QUERY:
    query = st.chat_input('Enter your query', 
                          disabled=not(API_KEY.startswith("sk-")))
    
     


# If query is provided and truthy, then I will write the value of the prompt
# to the streamlit chat_message object using the streamlit write method

if (CUSTOM_QUERY & (query is not None)) | ( (not CUSTOM_QUERY) & submitted):
    
    prompt = query
    
    
    # User input
    with st.chat_message("user", avatar = None):
        st.write(prompt)
    # Add user message to message history
    st.session_state.messages.append({"role":"user","content":prompt, "avatar":None})
 
    
    # Assistent (llm)'s response
    # Conext manager is used: all the code under with st.chat_message("assisent") will be done 
    # by the assistant
    with st.chat_message("assistant", avatar = "images/hal_9000.png"):
        # Output in-progress message
        st.write("Just a moment, just a moment...")
        # Run callback functions, wwhich will be run once we get responses (see below)
        st_callback = StreamlitCallbackHandler(st.container())
        # Get responses, using prompt as input. Pass the repsonse back to the callback functions
        # to be displayed
        response =  st.session_state.agent.run(prompt, callbacks=[st_callback])
        st.write(response)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response, "avatar":"images/hal_9000.png"})

