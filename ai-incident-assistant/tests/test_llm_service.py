from unittest.mock import MagicMock, patch

import pytest
from app.config import settings
from app.services.llm_service import generate_text, LLMServiceError

@patch("app.services.llm_service.genai.Client")
def test_generate_text_returns_gemini_output(mock_client_class, monkeypatch):
    monkeypatch.setattr(settings, "gemini_api_key","test-gemini-api-key")

    fake_response = MagicMock()
    fake_response.output_text = (
        "A health check confirms that a service is available."
    )

    mock_client = mock_client_class.return_value
    mock_client.interactions.create.return_value = fake_response

    prompt = "Explain a health-check endpoint in one sentence."

    result = generate_text(prompt)

    assert result == (
        "A health check confirms that a service is available."
    )

    mock_client.interactions.create.assert_called_once_with(
        model = settings.gemini_model,
        input = prompt,
    )




def test_generate_text_requires_api_key(monkeypatch):
    monkeypatch.setattr(settings, "gemini_api_key", None)

    with pytest.raises(
        LLMServiceError,
        match="GEMINI_API_KEY is not configured",
    ):
        generate_text("Test prompt")
