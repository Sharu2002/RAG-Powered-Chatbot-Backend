from fastapi import FastAPI
from sessionManager import set_session_id
from services.redisService import create_session, redis_client
from routes.ingest import router as ingest_router
from routes.chat import router as chat_router

# Global session_id
session_id = None

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    global session_id
    session_id = create_session()
    set_session_id(session_id)
    app.state.session_id = session_id
    print(f"Session started: {session_id}")
    yield
    if session_id:
        redis_client.delete(session_id)
        print(f"Session {session_id} destroyed")

app = FastAPI(lifespan=lifespan, title="RAG Chatbot API", version="1.0.0")


app.include_router(ingest_router, prefix="", tags=["Ingest"])
app.include_router(chat_router, prefix="", tags=["Chat"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
