from unittest.mock import patch, MagicMock
from src.controllers.ai_controller import prompt_gpt
from src.schemas.text_request import TextRequest
from fastapi import HTTPException
from groq import APIConnectionError, RateLimitError, APIStatusError
import pytest

@pytest.mark.asyncio # Need this decorator to test async functions
async def test_prompt_gpt():
    mock_response = MagicMock()

    # Create mock response
    mock_response.choices[0].message.content = ( 
        "* This is the first point.\n"
        "* This is the second point.\n"
        "*This is the third point."
    )

    # Replace the original return value of "create" with the mock response
    with patch(
        "src.controllers.ai_controller.client.chat.completions.create",
        return_value=mock_response
    ):
        # Create argument to pass to prompt_gpt
        text = TextRequest(
            text="Hurricanes develop over warm ocean waters, typically when sea surface temperatures exceed 26.5 degrees Celsius (about 80 degrees Fahrenheit). The process begins with the evaporation of water, which increases humidity in the atmosphere. As warm, moist air rises, it creates a low-pressure area beneath. This rising air cools and condenses, releasing latent heat, which further fuels the storm. Wind patterns, particularly the Coriolis effect, help organize the storm's rotation, leading to the formation of a well-defined center known as the eye. As the system strengthens, it can evolve into a tropical storm and eventually a hurricane, characterized by sustained winds of at least 74 miles per hour."
        )

        # Call prompt_gpt
        result = await prompt_gpt(text)

        # Check result
        assert result == {
            "summary": (
                "* This is the first point.\n"
                "* This is the second point.\n"
                "*This is the third point."
            )
        }

@pytest.mark.asyncio
async def test_prompt_gpt_illegible_response():
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "***\n*\n***"

    with patch(
        "src.controllers.ai_controller.client.chat.completions.create",
        return_value=mock_response
    ):
        text = TextRequest(
            text="The Google Pixel 11 is the latest addition to Google's smartphone lineup, showcasing advanced features and enhancements that cater to tech-savvy users. With its improved camera capabilities, sleek design, and integration of artificial intelligence, the device aims to provide an exceptional user experience. Additionally, the Pixel 11 is expected to offer seamless connectivity and performance, making it a strong contender in the competitive smartphone market."
        )

        with pytest.raises(HTTPException) as e:
            await prompt_gpt(text)

        assert e.value.status_code == 400
        assert e.value.detail == "Text may be illegible"

@pytest.mark.asyncio
async def test_prompt_gpt_api_connection_error():
    with patch(
        "src.controllers.ai_controller.client.chat.completions.create",
        side_effect=APIConnectionError(
            message="Unable to connect to Groq",
            request=None
        )
    ):
        text = TextRequest(
            text="The Google Pixel 11 is the latest addition to Google's smartphone lineup, showcasing advanced features and enhancements that cater to tech-savvy users. With its improved camera capabilities, sleek design, and integration of artificial intelligence, the device aims to provide an exceptional user experience. Additionally, the Pixel 11 is expected to offer seamless connectivity and performance, making it a strong contender in the competitive smartphone market."
        )

        with pytest.raises(HTTPException) as e:
            await prompt_gpt(text)

        assert e.value.status_code == 503
        assert e.value.detail == "AI service cannot be reached"

@pytest.mark.asyncio
async def test_prompt_gpt_rate_limit_error():
    mock_response = MagicMock()
    mock_response.status_code = 429

    mock_error = RateLimitError(
        message="Too many requests",
        response=mock_response,
        body=None
    )

    with patch(
        "src.controllers.ai_controller.client.chat.completions.create",
        side_effect=mock_error
    ):
        text = TextRequest(
                    text="The Google Pixel 11 is the latest addition to Google's smartphone lineup, showcasing advanced features and enhancements that cater to tech-savvy users. With its improved camera capabilities, sleek design, and integration of artificial intelligence, the device aims to provide an exceptional user experience. Additionally, the Pixel 11 is expected to offer seamless connectivity and performance, making it a strong contender in the competitive smartphone market."
        )
        
        with pytest.raises(HTTPException) as e:
            await prompt_gpt(text)

        assert e.value.status_code == 429
        assert e.value.detail == "Rate limit exceeded"

@pytest.mark.asyncio
async def test_prompt_gpt_api_status_error():
    mock_response = MagicMock()
    mock_response.status_code = 500

    mock_error = APIStatusError(
        message="Internal server error",
        response=mock_response,
        body=None
    )

    with patch(
        "src.controllers.ai_controller.client.chat.completions.create",
        side_effect=mock_error
    ):
        text = TextRequest(
            text="The Google Pixel 11 is the latest addition to Google's smartphone lineup, showcasing advanced features and enhancements that cater to tech-savvy users. With its improved camera capabilities, sleek design, and integration of artificial intelligence, the device aims to provide an exceptional user experience. Additionally, the Pixel 11 is expected to offer seamless connectivity and performance, making it a strong contender in the competitive smartphone market."
        )
                
        with pytest.raises(HTTPException) as e:
            await prompt_gpt(text)

        assert e.value.status_code == 500
        assert e.value.detail == "There was an error with AI services"