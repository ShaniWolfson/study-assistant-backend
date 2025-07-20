# documents/routers.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

# Import necessary components
from database import get_db # From project root
from models import User     # From project root
from auth.service import get_current_user # To protect endpoints
from .schemas import DocumentResponse, DocumentCreate, DocumentListResponse, DocumentUpdate        # Document schemas
from . import service        # Document business logic

router = APIRouter()

# Endpoint to create a new document
@router.post("/", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def create_document(
    document: DocumentCreate,
    current_user: User = Depends(get_current_user), # Protect this endpoint
    db: Session = Depends(get_db)
):
    db_document = service.create_user_document(db, document, user_id=current_user.id)
    return db_document

# Endpoint to get all documents for the current user
@router.get("/", response_model=List[DocumentListResponse])
async def read_documents(
    current_user: User = Depends(get_current_user), # Protect this endpoint
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    documents = service.get_user_documents(db, user_id=current_user.id, skip=skip, limit=limit)
    return documents

# Endpoint to get a single document by ID (ensure user owns it)
@router.get("/{document_id}", response_model=DocumentResponse)
async def read_document(
    document_id: int,
    current_user: User = Depends(get_current_user), # Protect this endpoint
    db: Session = Depends(get_db)
):
    db_document = service.get_document_by_id(db, document_id)
    if not db_document:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
    if db_document.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this document")
    return db_document

# Endpoint to update a document
@router.put("/{document_id}", response_model=DocumentResponse)
async def update_document_route(
    document_id: int,
    document_update: DocumentUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_document = service.get_document_by_id(db, document_id)
    if not db_document:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
    if db_document.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this document")

    updated_document = service.update_document(db, document_id, document_update)
    return updated_document

# Endpoint to delete a document
@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document_route(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_document = service.get_document_by_id(db, document_id)
    if not db_document:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
    if db_document.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this document")

    if not service.delete_document(db, document_id):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete document")
    # FastAPI returns 204 No Content for successful deletion without a body
    return