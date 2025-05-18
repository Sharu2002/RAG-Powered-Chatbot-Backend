from fastapi import APIRouter, HTTPException

from sessionManager import get_session_id, set_session_id
from services.redisService import create_session, redis_client

router = APIRouter()


@router.get("/clear-session")
async def clear_session():
    """
    Endpoint to clear the session.
    """
    try:
        redis_client.delete(get_session_id())  # Replace with actual session ID retrieval logic

        session_id = create_session()
        set_session_id(session_id)
        
        return {"message": "Session cleared successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
