from fastapi import APIRouter, HTTPException

from services.redisService import get_chat_history
from sessionManager import get_session_id

router = APIRouter()

@router.get("/chat-history")
async def get_history():
    """
    Endpoint to retrieve chat history.
    """
    try:
        # Placeholder for chat history retrieval logic
        # This should interact with the Redis database to fetch chat history
        print(f"Session ID: {get_session_id()} - Retrieving chat history...\n")
        chat_history = get_chat_history(get_session_id())  # Replace with actual retrieval logic

        if not chat_history:
            raise HTTPException(status_code=404, detail="No chat history found")

        return {"chat_history": chat_history}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))