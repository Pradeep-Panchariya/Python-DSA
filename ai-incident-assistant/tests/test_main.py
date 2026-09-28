from fastapi.testclient import TestClient

from app.main import app

from unittest.mock import patch

from app.schemas import GeminiIncidentAnalysis, IncidentReviewRequest

from app.services.llm_service import LLMServiceError
import app.main as main_module
from unittest.mock import MagicMock, patch
from app.config import settings 

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
def test_analyze_incident_returns_gemini_analysis(mock_generate_analysis,monkeypatch,):

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

    fake_record = MagicMock()
    fake_record.id = 123

    mock_create_record = MagicMock(
    return_value=fake_record,
    )

    monkeypatch.setattr(
        main_module,
        "create_incident_record",
        mock_create_record,
    )
    response = client.post("/analyze-incident",json = payload)
    assert response.status_code == 200

    response_data = response.json()

    assert response_data["category"] == "reporting"
    assert response_data["suggested_priority"] == "P2"
    assert response_data["human_review_required"] is True
    assert "Monthly report email failed" in response_data["summary"]
    assert "SMTP authentication failed" in response_data["summary"]
    assert response_data["source"] == "gemini"
    assert response_data["incident_id"] == 123
    mock_create_record.assert_called_once()


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

def test_health_check_returns_request_id():
    response = client.get("/health")

    assert response.status_code == 200
    assert "X-Request-ID" in response.headers
    assert response.headers["X-Request-ID"]


def test_health_check_preserves_client_request_id():
    request_id = "test-request-123"

    response = client.get(
        "/health",
        headers={"X-Request-ID": request_id},
    )

    assert response.status_code == 200
    assert response.headers["X-Request-ID"] == request_id


def test_get_incident_returns_stored_record(monkeypatch):
    fake_record = MagicMock()
    fake_record.id = 123
    fake_record.summary = (
        "Monthly report delivery failed because SMTP authentication failed."
    )
    fake_record.category = "reporting"
    fake_record.suggested_priority = "P2"
    fake_record.investigation_steps = [
        "Check SMTP credentials.",
        "Verify Secret Manager configuration.",
        "Review application logs.",
    ]
    fake_record.human_review_required = True
    fake_record.source = "gemini"

    mock_get_record = MagicMock(return_value=fake_record)

    monkeypatch.setattr(
        main_module,
        "get_incident_record",
        mock_get_record,
    )

    response = client.get("/incidents/123")

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["incident_id"] == 123
    assert response_data["category"] == "reporting"
    assert response_data["suggested_priority"] == "P2"
    assert response_data["source"] == "gemini"

    mock_get_record.assert_called_once()

def test_get_incident_returns_404_when_not_found(monkeypatch):
    mock_get_record = MagicMock(return_value=None)

    monkeypatch.setattr(
        main_module,
        "get_incident_record",
        mock_get_record,
    )

    response = client.get("/incidents/99999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Incident with id 99999 was not found."
    }


def test_review_incident_returns_reviewed_response(monkeypatch):
    fake_record = MagicMock()
    fake_record.id = 123
    fake_record.reviewed = True
    fake_record.reviewed_by = "pradeep@example.com"
    fake_record.review_notes = (
        "Confirmed that SMTP credentials were expired."
    )
    fake_record.category = "reporting"
    fake_record.suggested_priority = "P2"

    mock_review_record = MagicMock(return_value=fake_record)

    monkeypatch.setattr(
        main_module,
        "review_incident_record",
        mock_review_record,
    )

    payload = {
        "reviewed_by": "pradeep@example.com",
        "review_notes": "Confirmed that SMTP credentials were expired.",
        "category": "reporting",
        "suggested_priority": "P2",
    }

    response = client.patch(
        "/incidents/123/review",
        json=payload,
    )

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["incident_id"] == 123
    assert response_data["reviewed"] is True
    assert response_data["reviewed_by"] == "pradeep@example.com"
    assert response_data["review_notes"] == (
        "Confirmed that SMTP credentials were expired."
    )
    assert response_data["category"] == "reporting"
    assert response_data["suggested_priority"] == "P2"


    mock_review_record.assert_called_once()

def test_review_incident_returns_404_when_not_found(monkeypatch):
    mock_review_record = MagicMock(return_value=None)

    monkeypatch.setattr(
        main_module,
        "review_incident_record",
        mock_review_record,
    )

    payload = {
        "reviewed_by": "pradeep@example.com",
        "review_notes": "Confirmed that SMTP credentials were expired.",
        "category": "reporting",
        "suggested_priority": "P2",
    }

    response = client.patch(
        "/incidents/99999/review",
        json=payload,
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Incident with id 99999 was not found."
    }

    mock_review_record.assert_called_once()

def test_list_incidents_returns_records(monkeypatch):
    first_record = MagicMock()
    first_record.id = 101
    first_record.summary = "SMTP authentication failed."
    first_record.category = "reporting"
    first_record.suggested_priority = "P2"
    first_record.investigation_steps = [
        "Check SMTP credentials.",
        "Review application logs.",
        "Test SMTP connection.",
    ]
    first_record.human_review_required = True
    first_record.source = "gemini"

    second_record = MagicMock()
    second_record.id = 102
    second_record.summary = "Bucket permission denied."
    second_record.category = "access"
    second_record.suggested_priority = "P3"
    second_record.investigation_steps = [
        "Review IAM roles.",
        "Verify bucket permissions.",
        "Check policy changes.",
    ]
    second_record.human_review_required = True
    second_record.source = "gemini"

    mock_list_records = MagicMock(
        return_value=[first_record, second_record],
    )

    monkeypatch.setattr(
        main_module,
        "list_incident_records",
        mock_list_records,
    )

    response = client.get("/incidents?limit=10")

    assert response.status_code == 200

    response_data = response.json()

    assert len(response_data) == 2
    assert response_data[0]["incident_id"] == 101
    assert response_data[0]["category"] == "reporting"
    assert response_data[1]["incident_id"] == 102
    assert response_data[1]["category"] == "access"

    mock_list_records.assert_called_once()


def test_list_incidents_passes_reviewed_filter(monkeypatch):
    mock_list_records = MagicMock(return_value=[])

    monkeypatch.setattr(
        main_module,
        "list_incident_records",
        mock_list_records,
    )

    response = client.get("/incidents?limit=5&reviewed=false")

    assert response.status_code == 200
    assert response.json() == []

    call_kwargs = mock_list_records.call_args.kwargs

    assert call_kwargs["limit"] == 5
    assert call_kwargs["reviewed"] is False

def test_public_config_does_not_expose_api_key():
    response = client.get("/config")

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["app_name"] == "AI Incident Assistant"
    assert response_data["gemini_model"] == settings.gemini_model
    assert "gemini_api_key" not in response_data
    assert "gemini_api_key_configured" in response_data