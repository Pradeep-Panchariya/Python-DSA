from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200 
    assert response.json() == {
        "status": "AI Incident Assistant is running"
    }

def test_analyze_incident_returns_analysis():
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

    assert response_data["category"] == "needs_review"
    assert response_data["suggested_priority"] == "P3"
    assert response_data["human_review_required"] is True
    assert "Monthly report email failed" in response_data["summary"]
    assert "SMTP authentication failed" in response_data["summary"]



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