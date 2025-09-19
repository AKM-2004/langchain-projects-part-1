import streamlit as st
import validators as va
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import YoutubeLoader,UnstructuredURLLoader



## streamlit app 
st.set_page_config(page_title="summarize from youtube or website")
st.title("Langchain: Summarize Text from YT or Website")
st.subheader("summarize url")

import os
from dotenv import load_dotenv
load_dotenv() 
os.environ["GROQ_API"] = os.getenv("GROQ_API")
gorq_api = os.getenv("GROQ_API")
llm = ChatGroq(api_key=gorq_api,model="llama-3.1-8b-instant")

## prompt template 

prompttem = """

provide a summary of the following content in 300 words
{text}

"""

prompt = PromptTemplate(input_variables=["text"],template=prompttem)

generic_url = st.text_input("enter the url here",placeholder="enter the url of youtube or any website")

if st.button("summarize."):
    ### validate all the inputs 
    if not generic_url.strip():
        st.error("input nit tak re baba")
    
    elif not va.url(generic_url):
        st.error("nit tk barabbor nahi ahe url.")

    else:
        try:
            with st.spinner("aarahi hai info......."):
                ## loading the website data
                if "youtube.com" in generic_url:
                    loader = YoutubeLoader.from_youtube_url(youtube_url=generic_url,)

                else:
                    loader=UnstructuredURLLoader(urls=[generic_url],ssl_verify=False)
                
                data = loader.load()


                ## Chain for summarization 
                chain = load_summarize_chain(llm,chain_type="stuff",prompt=prompt)
                summary = chain.run(data)

                st.success(summary)
        except Exception as e:
            st.exception(f"Exception:{e}")





                










