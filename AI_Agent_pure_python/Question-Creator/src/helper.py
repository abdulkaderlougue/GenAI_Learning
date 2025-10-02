from langchain_community.document_loaders import PyPDFLoader, PDFPlumberLoader #type: ignore
from langchain.docstore.document import Document #type: ignore
from langchain.text_splitter import TokenTextSplitter #type: ignore
from langchain.chat_models import ChatOpenAI #type: ignore
from langchain.prompts import PromptTemplate #type: ignore
from langchain.chains.summarize import load_summarize_chain #type: ignore
from langchain.embeddings.openai import OpenAIEmbeddings #type: ignore
from langchain.vectorstores import FAISS #type: ignore
from langchain.chains import RetrievalQA # type: ignore
import os
from dotenv import load_dotenv # type: ignore
from src.prompt import prompt_template, refined_template
import getpass

# OpenAI authentication
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter your OpenAI API key: ")
else:
    os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

def process_file(file_path: str, chunk_size: int = 5000, chunk_overlap: int = 200) -> list[Document]:
    """Load and parse a PDF file into a list of document that has a single Document objects.
    then split the document into smaller chunks.
    """
    loader = PyPDFLoader(file_path, mode="single")
    # loader = PDFPlumberLoader(file_path)
    documents = loader.load() # a single Document 
    print(f"Loaded {documents} ")
    text_splitter = TokenTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    splited_docs = text_splitter.split_documents(documents)
    return splited_docs

def create_vector_store(texts: list[Document]) -> FAISS:
    """Create a FAISS vector store from the list of Document chunks."""
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vector_store = FAISS.from_documents(texts, embeddings)
    return vector_store

def llm_pipeline(file_path):
    """Create a LLM pipeline for question generation and answer generation."""
    MODEL = "gpt-3.5-turbo"
    question_document_processed =  process_file(file_path, chunk_size=8000, chunk_overlap=200)
    answer_document_processed =  process_file(file_path, chunk_size=1000, chunk_overlap=100)

    llm_ques_pipeline = ChatOpenAI(
        model = MODEL,
        temperature = 0.3,
    )

    # question generation chain  

    PROMPT_QUESTIONS = PromptTemplate(template=prompt_template, input_variables=["text"])

    REFINE_PROMPT_QUESTIONS = PromptTemplate(
        input_variables=["existing_answer", "text"],
        template=refined_template,
    )

    questions_chain = load_summarize_chain(llm = llm_ques_pipeline, 
                                            chain_type = "refine", 
                                            verbose = True, 
                                            question_prompt=PROMPT_QUESTIONS, 
                                            refine_prompt=REFINE_PROMPT_QUESTIONS)

    questions = questions_chain.run(question_document_processed)

    # create vector store for problem generation
    vector_store = create_vector_store(answer_document_processed)

    question_list = questions.split("\n")
    filtered_ques_list = [element for element in question_list if element.endswith('?') or element.endswith('.')]
    print(f"Generated {len(question_list)} questions.")
    print(f"Generated {len(filtered_ques_list)} filtered questions.")
    # print(filtered_ques_list)
    # answer generation llm

    llm_answer_pipeline = ChatOpenAI(
        model = MODEL,
        temperature = 0.1,
    )

    # answer generation chain
    
    answer_generation_chain = RetrievalQA.from_chain_type(llm=llm_answer_pipeline, 
                                                chain_type="stuff", 
                                                retriever=vector_store.as_retriever())

    return answer_generation_chain, filtered_ques_list


# test
if __name__ == "__main__":
    from prompt import prompt_template, refined_template
    file_path = "./wp-servicenow-enterprise-devops-platform.pdf"
    answer_generation_chain, question_list= llm_pipeline(file_path)

    for question in question_list:
        print("Question: ", question)
        answer = answer_generation_chain.run(question)
        print("Answer: ", answer)
        print("--------------------------------------------------\n\n")