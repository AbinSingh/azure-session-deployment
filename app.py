from fastapi import FastAPI

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