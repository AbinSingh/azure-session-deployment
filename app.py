from fastapi import FastAPI, HTTPException, Response, Request
from auth import authenticate
from models import LoginRequest
from session_store import create_session, delete_session
from middleware import SessionMiddleware
from redis_client import redis_client
import json

# Create the FastAPI application object.
# Uvicorn looks for this object when you run:
# uvicorn app:app --reload
app = FastAPI()
# register the middleware
app.middleware("http")(SessionMiddleware())


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
def login(login: LoginRequest, response: Response):
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

    response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True,
        secure=False
    )

    return {
        "message": "Authentication successful",
    }

@app.get("/debug/sessions")
def debug_sessions():

    sessions = {}

    for key in redis_client.keys("*"):

        sessions[key] = json.loads(
            redis_client.get(key)
        )

    return sessions

@app.get("/whoami")
def who_am_i(request: Request):

    return {
        "session_id": request.state.session_id,
        "session": request.state.session
    }

@app.get("/profile")
def profile(request: Request):

    if request.state.session is None:
        raise HTTPException(
            status_code=401,
            detail="Authentication required"
        )

    return {
        "message": "Profile retrieved successfully",
        "profile": {
            "username": request.state.session["username"]
        }
    }

@app.post("/logout")
def logout(request: Request, response: Response):

    if request.state.session_id:
        delete_session(request.state.session_id)

    response.delete_cookie(key="session_id")

    return {
        "message": "Logged out successfully"
}

@app.get("/redis/ping")
def redis_ping():

    result = redis_client.ping()

    return {
        "redis_connected": result
    }
