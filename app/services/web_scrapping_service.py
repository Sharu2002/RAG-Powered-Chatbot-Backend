from langchain_ollama import OllamaEmbeddings
import requests
from bs4 import BeautifulSoup
from langchain.docstore.document import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


from services.DbService import store_embeddings_in_db
from services.connectDbService import connect_db

from config.config import Config

MODEL_NAME = "nomic-embed-text"

def get_scraperapi_url(url):
    """ Construct the ScraperAPI request URL """
    return Config.SCRAPERAPI_URL.format(Config.SCRAPERAPI_KEY, url)

def extract_content(url):
    """ Extract content using ScraperAPI """
    try:
        response = requests.get(get_scraperapi_url(url))
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")

            # Content classes based on observed structure
            content_classes = [
                "article-body__content", "article__content__6hMn9",
                "body__content", "content__body", "main-content", "article-content"
            ]

            extracted_content = []
            for class_name in content_classes:
                sections = soup.find_all("div", class_=class_name)
                for section in sections:
                    extracted_content.append(section.get_text(strip=True))

            return "\n\n".join(extracted_content) if extracted_content else None
        else:
            print(f"Failed to fetch content from {url}, Status Code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error extracting content from {url}: {e}")
        return None
    
def split_content(content, url):
    """ Split content using RecursiveCharacterTextSplitter """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200,
        chunk_overlap=100,
        add_start_index=True
    )

    # Create a Document object
    document = Document(page_content=content, metadata={"source": url})

    # Split the content into chunks
    split_docs = text_splitter.split_documents([document])

    return split_docs

def generate_embeddings(documents):
    """ Generate embeddings using Ollama """
    embeddings_model = OllamaEmbeddings(model=MODEL_NAME)
    embeddings_list = embeddings_model.embed_documents([doc.page_content for doc in documents])
    return embeddings_list

def extract_and_store_embeddings(urls):
    """ Extract content, split into chunks, generate embeddings, and store in pgvector """
    # Collect all split documents
    documents = []

    for url in urls:
        print(f"Processing URL: {url}")
        content = extract_content(url)

        if content:
            # Split content into manageable chunks
            split_docs = split_content(content, url)
            print(f"Extracted and split {len(split_docs)} chunks for {url}")
            documents.extend(split_docs)
        else:
            print(f"No content found for {url}")

    # Generate embeddings
    embeddings = generate_embeddings(documents)

    # Connect to DB and store embeddings
    conn = connect_db()
    if conn:
        store_embeddings_in_db(conn, documents, embeddings)
        conn.close()
