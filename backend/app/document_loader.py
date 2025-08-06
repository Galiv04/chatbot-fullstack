# backend/app/document_loader.py

import os
from langchain_ollama import OllamaEmbeddings  # or OpenAIEmbeddings etc.
from langchain_chroma import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, TextLoader

# Change this to your actual vector DB directory
VECTOR_DB_DIR = os.path.join(os.path.dirname(__file__), "../vector_db")

def load_and_chunk(file_path):
    """Load a document file (.pdf or .txt), return a list of chunked texts."""
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.pdf':
        loader = PyPDFLoader(file_path)
    elif ext in ('.txt',):
        loader = TextLoader(file_path, encoding='utf-8')
    else:
        raise ValueError("Unsupported file type for document loader")

    documents = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=150)
    docs = splitter.split_documents(documents)
    return docs

def add_documents_to_vectorstore(file_paths, vector_dir=VECTOR_DB_DIR):
    """
    Loads, splits, embeds and adds provided documents to vectorstore.
    Returns the Chroma vectorstore instance.
    """
    embedding = OllamaEmbeddings(model="llama3.1:8b")  # Or your selected embedding model, e.g. "qwen2:7b"
    vectorstore = Chroma(persist_directory=vector_dir, embedding_function=embedding)
    for file_path in file_paths:
        docs = load_and_chunk(file_path)
        vectorstore.add_documents(docs)
    vectorstore.persist()
    return vectorstore

def create_or_load_vectorstore(vector_dir=VECTOR_DB_DIR):
    """
    Loads existing vectorstore (creates if not exist).
    """
    embedding = OllamaEmbeddings(model="llama3:8b")
    return Chroma(persist_directory=vector_dir, embedding_function=embedding)
