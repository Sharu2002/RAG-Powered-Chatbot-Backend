from fastapi import APIRouter, HTTPException

from sessionManager import get_session_id
from services.redisService import get_chat_history, store_message
from services.chatService import process_query

router = APIRouter()

@router.get("/chat")
async def chat(query: str):
    """
    Endpoint to handle chat queries.
    """
    try:
        # Placeholder for chat logic
        response = process_query(query, k=5)
        store_message(get_session_id(), query, response)

        chat_history = get_chat_history(get_session_id())
        print(f"\nSession ID: {get_session_id()} - Chat History:\n")
        for msg in chat_history:
            print(f"Time: {msg['timestamp']}\nQuery: {msg['query']}\nResponse: {msg['response']}\n")


        result = {"message": f"{response}"}
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))