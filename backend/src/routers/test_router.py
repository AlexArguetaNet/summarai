from fastapi import APIRouter
from src.controllers.test_controller import get_mock_summary
from src.schemas.text_request import TextRequest

router = APIRouter()

@router.post(
        "/test-summary",
        summary="Returns a mock summary for testing purposes"
)
async def mock_summary(text: TextRequest) -> dict:
    """
        Returns a mock summary to test the UI

        A test route that sends the user's text the backend 
        server and returns a mock summarization. This route is
        used solely to test placement of the text in the UI to
        prevent exceeding the rate limit of the Gemini API

        Args:
            text: The request body containing the text to summarize
        
        Returns:
            A dict with a "summary" key containing a list of
            bullet-point strings extracted from the model's response

    
    """
    return await get_mock_summary(text)
