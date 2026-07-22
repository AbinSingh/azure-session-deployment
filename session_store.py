import json
import uuid
from datetime import datetime, timedelta
from redis_client import redis_client


# In-memory session store
# Key   -> Session ID
# Value -> Session data

SESSION_TIMEOUT_MINUTES = 1

def create_session(username: str) -> str:
    """
    Create a new session for the authenticated user.
    Returns the generated session ID.
    """

    session_id = str(uuid.uuid4())

    now = datetime.utcnow()

    session = {
        "username": username,
        "created_at": now.isoformat(),
        "last_accessed": now.isoformat()
    }

    redis_client.set(
        session_id,
        json.dumps(session)
    )

    return session_id


def get_session(session_id: str):
    """
    Retrieve session information.
    """

    session_json = redis_client.get(session_id)

    if session_json is None:
        return None

    session = json.loads(session_json)

    now = datetime.utcnow()

    last_accessed = datetime.fromisoformat(
        session["last_accessed"]
    )

    if now - last_accessed > timedelta(minutes=SESSION_TIMEOUT_MINUTES):
        delete_session(session_id)
        return None

    session["last_accessed"] = now.isoformat()

    redis_client.set(
        session_id,
        json.dumps(session)
    )

    return session


def delete_session(session_id: str):
    """
    Delete a session.
    """

    redis_client.delete(session_id)