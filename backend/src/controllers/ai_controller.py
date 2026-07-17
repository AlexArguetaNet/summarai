from fastapi import HTTPException, status
from src.schemas.text_request import TextRequest
from google import genai
from google.genai import errors as gemini_errors
from src.utils.env_variables import get_api_key

# Get the API key
API_KEY = get_api_key()
client = genai.Client(api_key=API_KEY)

async def prompt_gemini(text: TextRequest) -> dict:
   
   # Check if the text is reasonably long enough to summarize
    if len(text.text) < 250:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Text must be at least 250 characters long")
    
    try:
        interaction = client.interactions.create(
            model="gemini-2.5-flash-lite",
            input=f"Summarize this text in three single-sentence bullet points mark with asterisks: {text.text}"
        )

        # API call was successful
        return {"summary": interaction.output_text} 
    
    except gemini_errors.ClientError as e:
        # Errors due too: bad request, invalid model, auth issues
        raise HTTPException(status_code=e.code or status.HTTP_400_BAD_REQUEST, detail=e.message)
    
    except gemini_errors.ServerError as e:
        # Errors due too upstream Gemini failure
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=f"Gemini service error: {e.message}")

    except gemini_errors.APIError as e:
        # Any other errors cause by the Gemini SDK
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Gemini API error: {e.message}")

    except Exception as e:
        # Rate limit exceeded
        if type(e).__name__ == "RateLimitError":
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded. Please try again later."
            )
        # Unexpected errors
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Unexpected error: {e}")