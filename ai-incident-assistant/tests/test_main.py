from fastapi.testclient import TestClient

from app.main import app

from unittest.mock import patch

from app.schemas import GeminiIncidentAnalysis

from app.services.llm_service import LLMServiceError

client = TestClient(app)

def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200 
    assert response.json() == {
        "status": "AI Incident Assistant is running"
    }

@patch(
    "app.services.incident_service."
    "generate_structured_incident_analysis"
)
def test_analyze_incident_returns_analysis(mock_generate_analysis,):

    mock_generate_analysis.return_value = GeminiIncidentAnalysis(
    summary=("Monthly report email failed because SMTP authentication "
            "failed during report delivery."
    ),
    category="reporting",
    suggested_priority="P2",
    investigation_steps=[
        "Check SMTP credentials.",
        "Verify Secret Manager configuration.",
        "Review application logs.",
    ],
    human_review_required=True,
)
    payload = {
        "title": "Monthly report email failed",
        "description":(
            "Cloud Scheduler ran successfully, but the report "
            "email was not delivered because SMTP authentication failed."
        ),
    }

    response = client.post("/analyze-incident",json = payload)
    assert response.status_code == 200

    response_data = response.json()

    assert response_data["category"] == "reporting"
    assert response_data["suggested_priority"] == "P2"
    assert response_data["human_review_required"] is True
    assert "Monthly report email failed" in response_data["summary"]
    assert "SMTP authentication failed" in response_data["summary"]
    assert response_data["source"] == "gemini"


def test_analyze_incident_rejects_short_input():
    payload = {
        "title": "bad",
        "description": "short",
    }

    response = client.post("/analyze-incident", json=payload)

    assert response.status_code == 422

    error_fields = [
        error["loc"][-1]
        for error in response.json()["detail"]
    ]

    assert "title" in error_fields
    assert "description" in error_fields


@patch(
    "app.services.incident_service."
    "generate_structured_incident_analysis"
)
def test_analyze_incident_returns_502_when_gemini_fails(
    mock_generate_analysis,
):
    mock_generate_analysis.side_effect = LLMServiceError(
        "Gemini request timed out."
    )

    payload = {
        "title": "Monthly report email failed",
        "description": (
            "Cloud Scheduler completed successfully, but the report "
            "email was not delivered because SMTP authentication failed."
        ),
    }

    response = client.post("/analyze-incident", json=payload)

    assert response.status_code == 502
    assert response.json() == {
        "detail": "AI analysis service is temporarily unavailable."
    }