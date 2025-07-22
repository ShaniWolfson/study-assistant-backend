# main.py
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
import uvicorn
import os
from dotenv import load_dotenv
from ai_processing import routers as ai_processing_routers

# Load environment variables (ensure this is at the top)
load_dotenv()

# Import your database and models
from database import engine, get_db, Base
import models

# Import your routers
from auth import routers as auth_routers # Import the auth router
from documents import routers as document_routers # Import the documents router

app = FastAPI(
    title="Study Assistant Backend",
    description="AI-powered study assistant API for summarization, quiz, and flashcard generation.",
    version="0.1.0",
)

# --- Basic API Endpoints (can keep these or move them) ---
@app.get("/")
def read_root():
    return {"message": "Welcome to the Study Assistant Backend API!"}

@app.get("/test-db-connection/")
def test_db_connection(db: Session = Depends(get_db)):
    try:
        users = db.query(models.User).limit(1).all()
        return {"message": "Database connection successful!", "found_users": len(users)}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database connection failed: {e}"
        )

# Include your API Routers
app.include_router(
    auth_routers.router,
    prefix="/auth",
    tags=["Authentication"]
)

app.include_router(
    document_routers.router,
    prefix="/documents",
    tags=["Documents"]
)

app.include_router(
    ai_processing_routers.router,
    prefix="/ai",
    tags=["AI Processing"]
)

# Optional: Run the app directly for development
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
# You would add other routers like this:
# app.include_router(
#     document_routers.router,
#     prefix="/documents",
#     tags=["Documents"]
# )
# app.include_router(
#     ai_routers.router,
#     prefix="/ai",
#     tags=["AI Processing"]
# )


# Optional: Run the app directly for development
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)