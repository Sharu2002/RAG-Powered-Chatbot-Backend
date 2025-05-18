from fastapi import APIRouter, HTTPException
from services.DbService import get_ingested_urls
from services.embeddingService import extract_and_store_embeddings
from models.urlModel import UrlModel
from urllib.parse import urlparse



router = APIRouter()

def is_valid_url(url):
    """ Check if the provided URL is valid. """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception as e:
        print(f"URL Validation Error: {e}")
        return False
    

@router.get("/ingest-urls")
async def read_item():
    return get_ingested_urls()

@router.post("/ingest-url")
async def ingest_url(url: UrlModel):
    """
    Endpoint to ingest a URL and extract its content.
    """
    try:
        if not is_valid_url(url.url):
            print(f"Invalid URL format: {url.url}")
            raise HTTPException(status_code=404, detail="Invalid URL format")
        
        ingested_urls = get_ingested_urls()

        if url.url in ingested_urls:
            print(f"URL already ingested: {url.url}")
            # Raise a specific HTTPException for URL already ingested
            raise HTTPException(status_code=400, detail="URL already ingested")

        print(f"New URL to ingest: {url.url}")
        content_extracted = extract_and_store_embeddings(url.url)

        print(f"Content extracted  VALUE : {content_extracted}")
        if not content_extracted:
            print(f"\nSHARU \nNo contkajndkajsndkasdent found for {url.url}")
            raise HTTPException(status_code=404, detail="No content found for the provided URL")

        return {"message": "Content ingested successfully", "url": url.url}

    except HTTPException as http_exc:
        # Handle specific HTTP exceptions without logging as a 500 error
        raise http_exc

    except Exception as e:
        print(f"Unexpected error during ingestion: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred during ingestion.")
