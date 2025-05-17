import os
import redis
import json
from datetime import datetime
from uuid import uuid4
from config.config import Config

# Load environment variables
REDIS_HOST = Config.REDIS_HOST
REDIS_PORT = int(Config.REDIS_PORT)
REDIS_DB = int(Config.REDIS_DB)
SESSION_EXPIRY = int(Config.SESSION_EXPIRY)

# Redis connection
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

def create_session():
    """ Generate a new session ID """
    session_id = str(uuid4())
    return session_id

def store_message(session_id, query, response):
    """ Store a query-response pair in Redis """
    message = {
        "timestamp": datetime.utcnow().isoformat(),
        "query": query,
        "response": response
    }

    # Store in a Redis list
    redis_client.rpush(session_id, json.dumps(message))

    # Set expiry for session
    redis_client.expire(session_id, SESSION_EXPIRY)

def get_chat_history(session_id):
    """ Retrieve chat history for a session """
    messages = redis_client.lrange(session_id, 0, -1)
    return [json.loads(message) for message in messages]

