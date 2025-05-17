from fastapi import APIRouter, HTTPException
from models.urlModel import UrlModel

from services.web_scrapping_service import extract_and_store_embeddings


router = APIRouter()

@router.get("/hello/{name}")
async def read_item(name: str):
    """
    Endpoint to greet the user.
    """
    return {"message": f"Hello, {name}!"}

@router.post("/ingest-url")
async def ingest_url(url : UrlModel):
    """
    Endpoint to ingest a URL and extract its content.
    """
    try:
        urls = []
        urls.append(url.url)
        extract_and_store_embeddings(urls)

        return {"message": "Content ingested successfully", "url": url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
