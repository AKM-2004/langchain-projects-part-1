import streamlit as st 
from langchain_groq import ChatGroq
from langchain_community.utilities import ArxivAPIWrapper,WikipediaAPIWrapper
from langchain_community.tools import ArxivQueryRun,WikipediaQueryRun,DuckDuckGoSearchRun
from langchain.agents import initialize_agent,AgentType
from langchain.callbacks import StreamlitCallbackHandler
import os 
from dotenv import load_dotenv
from langchain import hub 


load_dotenv()

## here we are setting the enviourment 
os.environ["HF_TOKEN"] = os.getenv("HF_TOKEN")
os.environ["GROQ_API"] = os.getenv("GROQ_API")
gorq_api = os.getenv("GROQ_API")


## sidebar for settings 
st.sidebar.title("Settings")
model = st.sidebar.selectbox("select from here",["select","llama-3.1-8b-instant"])

# Arxiv and wiki tools 
arxiv_api = ArxivAPIWrapper(top_k_results=1,doc_content_chars_max=300)
arxiv = ArxivQueryRun(api_wrapper=arxiv_api)

wiki_api = WikipediaAPIWrapper(top_k_results=1,doc_content_chars_max=300)
wiki = WikipediaQueryRun(api_wrapper=wiki_api)

search = DuckDuckGoSearchRun(name="search") ## this will search from the internet 

st.write("## Search engin with the langchain tools")

"""
in this example, we are using 'stremlitcallbackhandler' to display the thoughts and actions of an agent
in an interactive streamlit app. try more langchain streamlit agent examples at [github.com/langchain-ai/streamlit-agent]
"""


## this we are doing to preserve the user history see code dhayan se 
 
if "messages" not in st.session_state:
    st.session_state["messages"] =[
        {
            "role":"assistant",
            "content":"hi i am chatbot how can i help you??"
        }
    ]

for msg in st.session_state.messages: ## ye loop isliye hai taki hum mutliple content dekh sake
    st.chat_message(msg["role"]).write(msg["content"])

if prompt:=st.chat_input(placeholder="What is machine learning ?"):
    st.session_state.messages.append({"role":"user","content":prompt}) ## we done this to preserve history
    st.chat_message("user").write(prompt)

    llm = ChatGroq(api_key=gorq_api,model="llama-3.1-8b-instant")

    tools = [search,arxiv,wiki]
    search_agent = initialize_agent(tools,llm,agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,handling_parsing_errors=True)

    with st.chat_message("assistant"):
        st_cb = StreamlitCallbackHandler(st.container(),expand_new_thoughts=False) ## callbacks use for to interact with the app
        response = search_agent.run(st.session_state.messages,callbacks=[st_cb])
        st.session_state.messages.append({'role':'assistant',"content":response})
        st.write(response)





