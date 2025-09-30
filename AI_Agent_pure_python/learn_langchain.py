"""
Exploring LangChain capabilities in a pure Python environment.
pip install langchain langchain-community

it is just a framework, you still need to use your own LLMs, e.g. openai, azure, cohere, etc.
openai is already integrated in langchain, for other LLMs, you may need to install their SDKs and do some integration work.
"""

import os
from dotenv import load_dotenv

load_dotenv()

OPEN_API_KEY = os.getenv("OPENAI_API_KEY")
HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")
MODEL_NAME = "gpt-3.5-turbo"

# from langchain.llms import OpenAI
from langchain_openai import ChatOpenAI, OpenAI

temperature = 0.9 # higher value means more creative responses
# llm = ChatOpenAI(model_name=MODEL_NAME, 
#              temperature=temperature, 
#              openai_api_key=OPEN_API_KEY
# )

text = "What is a great idea for a startup?"
messages = [
    (
        "system",
        "You are a creative helpful assistant that provides creative ideas. Give the most creative, unique and realistic answer to the user .",
    ),
    ("human", text),
]
# ai_msg = llm.invoke(messages)

# print(ai_msg.content)

# HuggingFaceHub integration, free models
# from langchain_hub import HuggingFaceHub

# check langchain_complete_notebook 
#### Template in langchain 

#### chains

#### agents
#### memory




