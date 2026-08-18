from fastapi.testclient import TestClient
from src.main import app
import pytest

client = TestClient(app)

def test_summarize():
    response = client.post(
        "/summarize",
        json={"text": "Hurricanes develop over warm ocean waters, typically when sea surface temperatures exceed 26.5 degrees Celsius (about 80 degrees Fahrenheit). The process begins with the evaporation of water, which increases humidity in the atmosphere. As warm, moist air rises, it creates a low-pressure area beneath. This rising air cools and condenses, releasing latent heat, which further fuels the storm. Wind patterns, particularly the Coriolis effect, help organize the storm's rotation, leading to the formation of a well-defined center known as the eye. As the system strengthens, it can evolve into a tropical storm and eventually a hurricane, characterized by sustained winds of at least 74 miles per hour."}
    )

    assert response.status_code == 200
    assert "summary" in response.json()


@pytest.mark.parametrize(
        "text",
        [
            pytest.param("", id="empty"),
            pytest.param("    ", id="whitespace"),
            pytest.param("12345678910", id="numbers"),
            pytest.param("hello there how are you", id="under-char-count"),
        ]
)
def test_summarize_invalid_input(text):
    response = client.post(
        "/summarize",
        json={"text": text}
    )

    assert response.status_code == 400
    assert "detail" in response.json()