from pydantic import BaseModel

class TextRequest(BaseModel):
    """Request body for the summarization endpoint"""
    text: str