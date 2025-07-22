# study-assistant-backend/ai_processing/schemas.py
from pydantic import BaseModel, Field

# Request body to trigger summarization for a specific document
class SummarizeDocumentRequest(BaseModel):
    document_id: int = Field(..., description="The ID of the document to summarize.")

# Response for a summarization operation
class SummarizationResponse(BaseModel):
    document_id: int
    title: str
    summary: str
    message: str = "Document summarized successfully."