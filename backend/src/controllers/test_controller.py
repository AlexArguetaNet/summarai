from fastapi import HTTPException, status
from src.schemas.text_request import TextRequest

async def get_mock_summary(text: TextRequest) -> dict:
    # Check if the text is reasonably long enough to summarize
    if len(text.text) < 250:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Text must be at least 250 characters long")
    
    return {
                "summary": "Here is a three-sentence summary of the text "
                "in bullet points:\n\n*   The 2026 FIFA World Cup will be a historic, "
                "first-ever tripartite hosting by the United States, Canada, and Mexico, featuring the "
                "culmination of an expanded 48-team tournament in an iconic stadium, likely in the U.S."
                "\n*   This global event is expected to draw a massive audience and foster cultural exchange "
                "through passionate fan gatherings, accompanying festivities, and renowned artist performances."
                "\n*   The 2026 World Cup final aims to leave a significant legacy by promoting football's growth "
                "in North America and inspiring future generations, promising an unforgettable celebration of sport and unity."
           }
