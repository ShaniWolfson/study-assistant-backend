# database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable not set.")

# Create the SQLAlchemy engine
# pool_pre_ping=True helps prevent connection issues with long-running apps
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Create a SessionLocal class to get a database session
# Each instance of SessionLocal will be a database session
# The `autocommit=False` ensures you need to commit changes explicitly
# The `autoflush=False` means it won't flush changes to the DB until committed
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a declarative base for your models
# This will be inherited by all your SQLAlchemy models
Base = declarative_base()

# Dependency to get a database session for FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()