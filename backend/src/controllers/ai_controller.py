from fastapi import HTTPException, status
from src.schemas.text_request import TextRequest
from groq import Groq
from groq import (APIConnectionError, RateLimitError, APIStatusError)
from src.utils.env_variables import get_api_key

# Get the API key
API_KEY = get_api_key()
client = Groq(api_key=API_KEY)

async def prompt_llama(text: TextRequest) -> dict:
    """
        Summarizes text into three bullet points using Meta Llama 3.1 8B via the Groq API.

        Validates the character count of text is at least 250. A chat completion request
        is sent to Meta's llama-3.1-8b model hosted on Groq Cloud and the chat response
        is returned. Exceptions from the Groq package are caught and translated into
        FastAPI HTTPExceptions.

        Args:
            text (TextRequest): Pydantic request body containing the user's text input

        Returns:
            dict: The summary result

        Raises:
            HTTPException: 400 Bad Request - if the text is under 250 characters.
            HTTPException: 429 Too Many Requests - reached Groq API rate limit
            HTTPException: 503 Service Unavailable - cannot connect to Groq services
            HTTPException: 500 Internal Server Error - unexpected backend failures

    """
   # Check if the text is reasonably long enough to summarize
    if len(text.text) < 250:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Text must be at least 250 characters long")

    user_text = text.text # Get the user's text from the pydantic model

    try:
        chat_completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages = [
                {
                    "role": "user",
                    "content": f"Summarize this text in three single-sentence bullet points mark with asterisks: {user_text}",
                }
            ],
        )

        # API call successful
        return {"summary": chat_completion.choices[0].message.content}

    # Handle Exceptions
    except APIConnectionError as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Groq services cannot be reached")
    
    except RateLimitError as e:
        raise HTTPException(status_code=e.status_code, detail="Rate limit exceeded")
    
    except APIStatusError as e:
        raise HTTPException(status_code=e.status_code, detail="There was an error with groq services")
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="There was an error with the server")
