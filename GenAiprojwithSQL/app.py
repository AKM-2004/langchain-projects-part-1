import streamlit as st 
from pathlib import Path
from dotenv import load_dotenv
from langchain.agents import create_sql_agent
from langchain.agents.agent_types import AgentType
from langchain.sql_database import SQLDatabase
from langchain.callbacks import StreamlitCallbackHandler
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
#Toolkits allow you to logically group and initialize a set of tools that share a particular resource 
# (such as a database connection or json object). They can be used to construct an agent for a specific use-case. 
# for examplre the one which we are going to use now with the sql
from sqlalchemy import create_engine ## this is an use full library in python for create engines of sql
## this sqlalchemy helps to map with respect to output which come from your sql_database. 
## with the help of alchemy you can use pythonic langauge you can ipliment table in 
# the form of classes and all without using the sql commands you can how it works 
import sqlite3
from langchain_groq import ChatGroq

st.set_page_config(page_title="Langchain: Chat with your Sql DB")
st.title("LangChain: chat with your SQL_DB")

MYSQL = "USE_MYSQL"
Localdb = "USE_LOCALDB"
radio_opt = ["use the local database","Connect to your SQL DATABASE"]
selected_info = st.sidebar.radio(label="Chose the DB",options=radio_opt)

if radio_opt.index(selected_info) == 1:

    db_uri = MYSQL
    mysql_host = st.sidebar.text_input("provide my sql host")
    mysql_user = st.sidebar.text_input("my sql user")
    mysql_pass = st.sidebar.text_input("enter the password",type="password")
    mysql_db = st.sidebar.text_input("My Sql Database")

else:
    db_uri = Localdb

import os
load_dotenv()
get_api = os.getenv("GROQ_API")
llm = ChatGroq(api_key=get_api,model_name="llama-3.1-8b-instant")


@st.cache_resource(ttl="2h") # this will put the memory of database for 2 hour in your db 
## this function configure_db is use for the
def configure_db(db_uri,mysql_host=None,mysql_user=None,mysql_pass=None,mysql_db=None):
    if db_uri == Localdb:
        db_file_path =(Path(__file__).parent/"customer.db").absolute()
        create = lambda: sqlite3.connect(f"file:{db_file_path}?mode=ro",uri=True)
        return SQLDatabase(create_engine("sqlite:///",creator=create))
    elif db_uri==MYSQL:
        if not(mysql_db and mysql_host and mysql_pass and mysql_user):
            st.error("bro error aaraha hai")
            st.stop()
        return SQLDatabase(create_engine(f"mysql+mysqlconnector://{mysql_user}:{mysql_pass}@{mysql_host}/{mysql_db}"))
    
if db_uri == MYSQL:
    db = configure_db(db_uri,mysql_host=None,mysql_user=None,mysql_pass=None,mysql_db=None)
else:
    db = configure_db(db_uri)

## toolkit 

toolkit = SQLDatabaseToolkit(db=db,llm=llm)
agent = create_sql_agent(llm=llm,toolkit=toolkit,agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION)

## lets create the chat and session_state

if "message" not in st.session_state or st.sidebar.button("clear my history"):
    st.session_state["message"] = [{"role":"assistant",
                                    "content":"How can i help you?"}]
    
for msg in st.session_state.message:
    st.chat_message(msg["role"]).write(msg["content"])
    
user_query = st.chat_input(placeholder="put the query here")

if user_query:
    st.session_state.message.append({"role":"user","user_query":user_query})
    st.chat_message("user").write(user_query)

    with st.chat_message("assistant"):
        st_cb = StreamlitCallbackHandler(st.container(),expand_new_thoughts=False) ## callbacks use for to interact with the app
        response = agent.run(st.session_state.message,callbacks=[st_cb])
        st.session_state.message.append({'role':'assistant',"content":response})
        st.write(response)

