from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    SCRAPERAPI_KEY = os.getenv("SCRAPERAPI_KEY")
    SCRAPERAPI_URL = os.getenv("SCRAPERAPI_URL")

    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_NAME = os.getenv("DB_NAME")

    REDIS_HOST = os.getenv("REDIS_HOST")
    REDIS_PORT = os.getenv("REDIS_PORT")
    REDIS_DB = os.getenv("REDIS_DB")
    SESSION_EXPIRY = os.getenv("SESSION_EXPIRY")


    MODEL_NAME = os.getenv("MODEL_NAME")

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GEMINI_API_URL = os.getenv("GEMINI_API_URL")

