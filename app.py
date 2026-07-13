from fastapi import FastAPI, HTTPException
from auth import authenticate
from models import LoginRequest
from session_store import create_session, sessions

# Create the FastAPI application object.
# Uvicorn looks for this object when you run:
# uvicorn app:app --reload
app = FastAPI()


@app.get("/")
def health_check():
    """
    Simple endpoint to verify that the application is running.
    """

    return {
        "status": "running",
        "application": "session-local",
        "message": "Welcome to the FastAPI Session Demo"
    }

@app.post("/login")
def login(login: LoginRequest):
    """
    Authenticate the user.
    No session is created in this commit.
    """

    if not authenticate(login.username, login.password):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    session_id = create_session(login.username)

    return {
        "message": "Authentication successful",
        "session_id": session_id
    }

@app.get("/debug/sessions")
def debug_sessions():
    return sessions