# study-assistant-backend/ai_processing/service.py
import os
from openai import OpenAI
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

# Absolute import for models (from the project root)
import models

# Relative import for document_service (from a sibling package)
from documents import service as document_service


# Initialize OpenAI client
client = OpenAI()

async def get_text_summary(text_content: str) -> str:
    """
    Uses OpenAI's GPT model to generate a summary of the provided text.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo", # You can choose a different model like "gpt-4" if you have access
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes text concisely."},
                {"role": "user", "content": f"Please summarize the following document:\n\n{text_content}"}
            ],
            max_tokens=200, # Limit the length of the summary to 200 tokens
            temperature=0.7, # Controls randomness: lower for more focused, higher for more creative
        )
        summary = response.choices[0].message.content.strip()
        return summary
    except Exception as e:
        print(f"ERROR: Error calling OpenAI API: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate summary: {e}"
        )

async def summarize_and_update_document(db: Session, document_id: int) -> models.Document:
    """
    Retrieves a document, generates its summary, and updates the document in the DB.
    """
    db_document = document_service.get_document_by_id(db, document_id)
    if not db_document:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found.")

    summary = await get_text_summary(db_document.content)

    # Update the document with the summary
    db_document.summary = summary
    db.add(db_document)
    db.commit()
    db.refresh(db_document)

    return db_document