from fastapi import FastAPI, HTTPException, Response, Request
from auth import authenticate
from models import LoginRequest
from session_store import create_session, sessions
from middleware import SessionMiddleware


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