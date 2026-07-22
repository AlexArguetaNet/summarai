from fastapi import APIRouter
from src.controllers.ai_controller import prompt_llama
from src.schemas.text_request import TextRequest

router = APIRouter()

@router.post(
        "/summarize", 
        summary="Summarizes text into bullet points", 
)
async def summarize(text: TextRequest) -> dict:
    """Summarize input text into three single-sentence bullet points using Gemini

        Sends the user's text to the Gemini API and parses the
        response into a list of bullet-point summaries

        Args:
            text: The request body containing the text to summarize
        
        Returns:
            A dict with a "summary" key containing a list of
            bullet-point strings extracted from the model's response

        Raises:
            HTTPException:
                - 400 if the request to Gemini is invalid (rate limit exceeded)
                - 502 if the Gemini service itself fails
                - 500 for any other unexpected error

    """
    return await prompt_llama(text)