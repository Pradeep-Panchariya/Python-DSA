from app.schemas import IncidentRequest, GeminiIncidentAnalysis
from app.services.incident_service import analyze_incident, analyze_incident_with_gemini
from unittest.mock import MagicMock, patch

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
    assert result["source"] == "rule_based"



@patch(
    "app.services.incident_service."
    "generate_structured_incident_analysis"
)
def test_analyze_incident_with_gemini_returns_gemini_source(
    mock_generate_analysis,
):
    incident = IncidentRequest(
        title="GCP bucket access denied",
        description=(
            "The scheduled process cannot read an input file because "
            "the service account receives a permission denied error."
        ),
    )

    mock_generate_analysis.return_value = GeminiIncidentAnalysis(
        summary=(
            "The scheduled process cannot access the input file "
            "because the service account lacks permission."
        ),
        category="access",
        suggested_priority="P2",
        investigation_steps=[
            "Review the service account IAM roles.",
            "Verify bucket-level permissions.",
            "Check recent IAM policy changes.",
        ],
        human_review_required=True,
    )

    result = analyze_incident_with_gemini(incident)

    assert result.source == "gemini"
    assert result.category == "access"
    assert result.suggested_priority == "P2"
    assert result.human_review_required is True

    mock_generate_analysis.assert_called_once()