

# documents/schemas.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

# Schema for creating a new document (request body)
class DocumentCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    content: str = Field(..., min_length=10) # Assuming raw text content

# Schema for updating an existing document
class DocumentUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    content: Optional[str] = Field(None, min_length=10)
    summary: Optional[str] = None # Will be populated by AI later

# Schema for responding with a document (response model)
class DocumentResponse(BaseModel):
    id: int
    user_id: int
    title: str
    content: str
    summary: Optional[str] = None
    uploaded_at: datetime

    class Config:
        from_attributes = True # For Pydantic v2+ (earlier versions used `orm_mode = True`)

# Schema for responding with a list of documents (simplified)
class DocumentListResponse(BaseModel):
    id: int
    title: str
    summary: Optional[str] = None
    uploaded_at: datetime

    class Config:
        from_attributes = True