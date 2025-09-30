"""
demo for a local vector db: chromadb
there are many other options, e.g. weaviate, pinecone, qdrant, 

data --> embeddings model(openai encoding) --> vector embedingd --> vector db (chromadb)
"""

from langchain.vectorstores import Chroma
# from langchain.openai import OpenAIEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.document_loaders import TextLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Load documents from a directory
loader = DirectoryLoader('data', glob='**/*.txt', loader_cls=TextLoader)
documents = loader.load()
# print(documents)

# Split documents into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
texts = text_splitter.split_documents(documents)
print(f"split into {len(texts)} chunks")

# create db


persistence_directory = 'db'
embedding = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
# embedding = OpenAIEmbeddings(model="text-embedding-3-small", openai_api_key=OPENAI_API_KEY)

# embedding = OpenAIEmbeddings()

print(embedding)
# vectordb = Chroma.from_documents(documents=texts, embedding=embedding, persist_directory=persistence_directory)

# vectordb.persist()