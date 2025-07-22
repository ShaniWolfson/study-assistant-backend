# study-assistant-backend/ai_processing/routers.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

# Absolute imports for database.py and models.py (from the project root)
from database import get_db
from models import User, Document

from . import schemas
from . import service as ai_service
from auth.service import get_current_user

router = APIRouter()

@router.post("/summarize", response_model=schemas.SummarizationResponse)
async def summarize_document_route(
    request: schemas.SummarizeDocumentRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Retrieve the document to ensure it belongs to the current user
    db_document = db.query(Document).filter(
        Document.id == request.document_id,
        Document.user_id == current_user.id
    ).first()

    if not db_document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found or you don't have access to it."
        )

    # Call the service to generate the summary and update the document in the database
    try:
        updated_document = await ai_service.summarize_and_update_document(db, request.document_id)
    except HTTPException as e:
        # If the service raises an HTTPException, re-raise it directly
        raise e
    except Exception as e:
        # Catch any other unexpected errors during summarization
        # Log it and return a generic 500 error to the client
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred during summarization: {e}"
        )

    # Return a success response, including the generated summary
    return schemas.SummarizationResponse(
        document_id=updated_document.id,
        title=updated_document.title,
        summary=updated_document.summary
    )