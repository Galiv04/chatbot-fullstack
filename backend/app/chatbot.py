import os
import logging
from langchain_ollama import OllamaLLM
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter

logger = logging.getLogger(__name__)

OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3.1:8b")
VECTOR_DB_DIR = os.path.join(os.path.dirname(__file__), "../vector_db")

def get_llm(model_name: str = OLLAMA_MODEL):
    """Initialize and return an Ollama LLM wrapper."""
    return OllamaLLM(model=model_name)

def answer_with_llama(
    user_message: str,
    chat_history: list = None,
    knowledge_context: str = "",
    model_name: str = OLLAMA_MODEL,
) -> str:
    """
    Compose a system prompt with optional previous messages and optional doc context,
    then get answer from Ollama LLM.
    """
    llm = get_llm(model_name)
    # Compose context for model prompt
    conversation = ""
    if chat_history:
        for msg in chat_history:
            # NB: assumes .sender and .content fields
            conversation += f"{msg.sender}: {msg.content}\n"
    system_instructions = (
        f"You can use the following knowledge to answer the user's question:\n{knowledge_context}\n"
        if knowledge_context else ""
    )
    prompt = (
        f"{system_instructions}"
        f"{conversation}"
        f"User: {user_message}\n"
        "Assistant:"
    )
    logger.info(f"Full LLM prompt:\n{prompt[:600]}...")  # log up to 600 chars
    response = llm.invoke(prompt)
    logger.info(f"LLM response: {response[:500]}")  # log up to 500 chars
    return response

def get_vectorstore():
    """Load the current on-disk vector db for retrieval."""
    if os.path.isdir(VECTOR_DB_DIR):
        try:
            embedding = OllamaEmbeddings(model=OLLAMA_MODEL)
            return Chroma(persist_directory=VECTOR_DB_DIR, embedding_function=embedding)
        except Exception as e:
            logger.error(f"Error loading vectorstore: {e}")
            return None
    return None

def search_documents(query, top_k=3):
    """
    Retrieve relevant knowledge (doc context) for the query.
    """
    vectorstore = get_vectorstore()
    if not vectorstore:
        logger.info("No vectorstore found, knowledge context empty.")
        return ""
    docs = vectorstore.similarity_search(query, k=top_k)
    context = "\n".join([d.page_content for d in docs if hasattr(d, 'page_content')])
    logger.info(f"Knowledge context for '{query[:50]}...':\n{context[:400]}...")
    return context

def get_chatbot_answer(user_message, chat_history=None, use_kb=True, model_name=OLLAMA_MODEL):
    """
    Returns a chatbot answer using the model, optionally with doc retrieval context.
    """
    doc_context = search_documents(user_message) if use_kb else ""
    return answer_with_llama(
        user_message,
        chat_history=chat_history,
        knowledge_context=doc_context,
        model_name=model_name
    )
