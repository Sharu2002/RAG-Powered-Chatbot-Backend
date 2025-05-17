import requests
from bs4 import BeautifulSoup
from langchain.docstore.document import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


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

