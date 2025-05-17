import psycopg2
from config.config import Config

def connect_db():
    """ Establish connection to PostgreSQL """
    try:
        print("Connecting to the database...")
        print(f"Host: {Config.DB_HOST}, Port: {Config.DB_PORT}, User: {Config.DB_USER}, DB Name: {Config.DB_NAME}, Password: {Config.DB_PASSWORD}")
        conn = psycopg2.connect(
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            dbname=Config.DB_NAME
        )
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None
