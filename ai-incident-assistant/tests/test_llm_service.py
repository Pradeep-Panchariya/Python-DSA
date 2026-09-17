from unittest.mock import MagicMock, patch

import pytest
from app.config import settings
from app.services.llm_service import generate_text, LLMServiceError,generate_structured_incident_analysis,generate_text


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


@patch("app.services.llm_service.genai.Client")
def test_generate_structured_incident_analysis_returns_valid_model(
    mock_client_class,
    monkeypatch,
):
    monkeypatch.setattr(
        settings,
        "gemini_api_key",
        "test-gemini-api-key",
    )

    fake_response = MagicMock()
    fake_response.output_text = """
    {
        "summary": "Report delivery failed because SMTP authentication failed.",
        "category": "reporting",
        "suggested_priority": "P2",
        "investigation_steps": [
            "Check SMTP credentials.",
            "Verify Secret Manager configuration.",
            "Review application logs."
        ],
        "human_review_required": true
    }
    """

    mock_client = mock_client_class.return_value
    mock_client.interactions.create.return_value = fake_response

    result = generate_structured_incident_analysis(
        "Analyze this incident."
    )

    assert result.category == "reporting"
    assert result.suggested_priority == "P2"
    assert result.human_review_required is True
    assert len(result.investigation_steps) == 3

    mock_client.interactions.create.assert_called_once()

    call_kwargs = (
        mock_client.interactions.create.call_args.kwargs
    )

    assert call_kwargs["model"] == settings.gemini_model
    assert call_kwargs["response_format"]["mime_type"] == (
        "application/json"
    )