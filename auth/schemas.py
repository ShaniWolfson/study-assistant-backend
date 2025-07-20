# auth/schemas.py
from pydantic import BaseModel, EmailStr
from typing import Optional # Add this import

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config: # This tells Pydantic to convert SQLAlchemy objects to Pydantic objects
        from_attributes = True # For Pydantic v2+ (earlier versions used `orm_mode = True`)

# --- User Login ---
class UserLogin(BaseModel):
    username: str # Users will log in with username or email, let's keep it simple with username for now
    password: str

# --- JWT Token Response ---
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer" # Default token type

# --- JWT Token Data (Payload) ---
# This defines the data we expect inside the JWT payload
class TokenData(BaseModel):
    username: Optional[str] = None # Or email, or user_id