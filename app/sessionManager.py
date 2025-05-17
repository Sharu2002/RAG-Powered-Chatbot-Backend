# app/session_manager.py

# Global session_id
session_id = None

def set_session_id(new_session_id):
    global session_id
    session_id = new_session_id

def get_session_id():
    return session_id
