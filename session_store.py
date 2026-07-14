import uuid
from datetime import datetime, timedelta

# In-memory session store
# Key   -> Session ID
# Value -> Session data
sessions = {}
SESSION_TIMEOUT_MINUTES = 1

def create_session(username: str) -> str:
    """
    Create a new session for the authenticated user.
    Returns the generated session ID.
    """

    session_id = str(uuid.uuid4())

    now = datetime.utcnow()

    sessions[session_id] = {
        "username": username,
        "created_at": now,
        "last_accessed": now
    }

    return session_id


def get_session(session_id: str):
    """
    Retrieve session information.
    """

    session = sessions.get(session_id)

    if session is None:
        return None

    now = datetime.utcnow()

    last_accessed = session["last_accessed"]

    if now - last_accessed > timedelta(minutes=SESSION_TIMEOUT_MINUTES):
        delete_session(session_id)
        return None

    session["last_accessed"] = now

    return session


def delete_session(session_id: str):
    """
    Delete a session.
    """

    sessions.pop(session_id, None)