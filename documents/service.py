# ai_processing/service.py
import os
from openai import OpenAI
from sqlalchemy.orm import Session
from fastapi import HTTPException, status # Make sure these are imported for the service layer

from models import Document
from documents import service as document_service
from .schemas import DocumentCreate, DocumentUpdate

client = OpenAI()


def create_user_document(db: Session, document: DocumentCreate, user_id: int):
    """
    Creates a new document entry in the database for a given user.
    """
    db_document = Document(
        user_id=user_id,
        title=document.title,
        content=document.content,
        # summary will be populated later by an AI service
    )
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document

def get_user_documents(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    """
    Retrieves a list of documents for a specific user.
    """
    return db.query(Document).filter(Document.user_id == user_id).offset(skip).limit(limit).all()

def get_document_by_id(db: Session, document_id: int):
    """
    Retrieves a single document by its ID.
    """
    return db.query(Document).filter(Document.id == document_id).first()

def update_document(db: Session, document_id: int, document_update: DocumentUpdate):
    """
    Updates an existing document.
    """
    db_document = db.query(Document).filter(Document.id == document_id).first()
    if db_document:
        update_data = document_update.model_dump(exclude_unset=True) # For Pydantic v2+
        for key, value in update_data.items():
            setattr(db_document, key, value)
        db.add(db_document)
        db.commit()
        db.refresh(db_document)
    return db_document

def delete_document(db: Session, document_id: int):
    """
    Deletes a document by its ID.
    """
    db_document = db.query(Document).filter(Document.id == document_id).first()
    if db_document:
        db.delete(db_document)
        db.commit()
        return True # Indicate successful deletion
    return False # Document not found or not deleted