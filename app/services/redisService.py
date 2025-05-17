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
