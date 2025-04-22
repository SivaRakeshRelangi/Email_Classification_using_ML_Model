from fastapi import FastAPI
from api import router  # Import the API routes from api.py
import inspect
# Initialize FastAPI app instance
app = FastAPI(
    title="Email Classifier API",
)
# Home route: Return a welcome message
@app.get("/")
def read_root():
    return {"message": "Welcome to the Email Classifier API! Use /classify_email for email classification."}

# Include API routes from api.py
app.include_router(router)
