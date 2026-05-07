import sys
import streamlit as st
from dotenv import load_dotenv
from pathlib import Path
import os

env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

key = os.getenv("GROQ_API_KEY")

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

import streamlit as st
import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

key = os.getenv("GROQ_API_KEY")

if not key:
    raise ValueError("GROQ_API_KEY not found")

key = key.strip()


prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("human", "Question: {input}")
])

st.title("LangChain + Groq Chatbot")

input_text = st.text_input("Enter your question:")

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=key
)

output_parser = StrOutputParser()
chain = prompt | llm | output_parser

if input_text:
    st.write(chain.invoke({"input": input_text}))
