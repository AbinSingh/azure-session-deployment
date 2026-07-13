import uuid

# In-memory session store
# Key   -> Session ID
# Value -> Session data
sessions = {}


def create_session(username: str) -> str:
    """
    Create a new session for the authenticated user.
    Returns the generated session ID.
    """

    session_id = str(uuid.uuid4())

    sessions[session_id] = {
        "username": username
    }

    return session_id


def get_session(session_id: str):
    """
    Retrieve session information.
    """

    return sessions.get(session_id)


def delete_session(session_id: str):
    """
    Delete a session.
    """

    sessions.pop(session_id, None)