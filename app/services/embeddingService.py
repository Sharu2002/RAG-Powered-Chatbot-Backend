from langchain_ollama import OllamaEmbeddings

from services.web_scrapping_service import extract_content, split_content
from services.DbService import store_embeddings_in_db
from services.connectDbService import connect_db

from config.config import Config

def generate_embedding(query):
    """ Generate embedding for the query using Ollama """
    embeddings_model = OllamaEmbeddings(model=Config.MODEL_NAME)
    query_embedding = embeddings_model.embed_documents([query])[0]
    return query_embedding


def generate_embeddings(documents):
    """ Generate embeddings using Ollama """
    embeddings_model = OllamaEmbeddings(model=Config.MODEL_NAME)
    embeddings_list = embeddings_model.embed_documents([doc.page_content for doc in documents])
    return embeddings_list

def extract_and_store_embeddings(url):
    """ Extract content, split into chunks, generate embeddings, and store in pgvector """
    documents = []

    print(f"Processing URL: {url}")
    content = extract_content(url)

    if not content:
        print(f"No content found for {url}")
        return None

    # Split content into chunks
    split_docs = split_content(content, url)
    if not split_docs:
        print(f"No content extracted for {url}")
        return None

    documents.extend(split_docs)

    # Generate embeddings
    embeddings = generate_embeddings(documents)

    # Connect to DB and store embeddings
    conn = connect_db()
    if conn:
        store_embeddings_in_db(conn, documents, embeddings)
        conn.close()

    return "Content ingested successfully"