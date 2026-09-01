from app.schemas import IncidentRequest
from app.services.incident_service import analyze_incident

def test_analyze_incident_returns_expected_structure():
    incident = IncidentRequest(
        title = 'GCP bucket access denied',
        description = (
            "The scheduled process cannot read the input file "
            "because the service account receives a permission denied error."
        ),
    )

    result = analyze_incident(incident)

    assert result["category"] == "needs_review"
    assert result["suggested_priority"] == "P3"
    assert result["human_review_required"] is True
    assert "GCP bucket access denied" in result["summary"]
    assert "permission denied error" in result["summary"]
    assert len(result["investigation_steps"]) == 3