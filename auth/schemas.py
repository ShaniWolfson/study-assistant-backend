# auth/schemas.py
from pydantic import BaseModel, EmailStr

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

# You'd also have models for login, tokens, etc., here later
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None