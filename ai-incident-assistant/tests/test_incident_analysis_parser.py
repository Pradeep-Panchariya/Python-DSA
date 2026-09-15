from app.services.incident_service import parse_gemini_incident_analysis, IncidentAnalysisError
import pytest 

def test_parse_gemini_incident_analysis_returns_valid_response():

    raw_response = """
    {
        "summary": "Report delivery failed because SMTP authentication failed.",
        "category": "reporting",
        "suggested_priority": "P2",
        "investigation_steps": [
            "Check SMTP credentials.",
            "Verify the Secret Manager configuration.",
            "Review application logs."
        ],
        "human_review_required": true
    }
    """

    analysis = parse_gemini_incident_analysis(raw_response)

    assert analysis.summary == (
        "Report delivery failed because SMTP authentication failed."
    )
    assert analysis.category == "reporting"
    assert analysis.suggested_priority == "P2"
    assert len(analysis.investigation_steps) == 3
    assert analysis.human_review_required is True
    assert analysis.source == "gemini"


def test_parse_gemini_incident_analysis_rejects_non_json():
    raw_response = "SMTP authentication may have failed."

    with pytest.raises(
        IncidentAnalysisError,
        match="Gemini returned invalid JSON",
    ):
        parse_gemini_incident_analysis(raw_response)


def test_parse_gemini_incident_analysis_rejects_invalid_priority():
    raw_response = """
    {
        "summary": "Report delivery failed.",
        "category": "reporting",
        "suggested_priority": "P9",
        "investigation_steps": [
            "Check logs.",
            "Check credentials.",
            "Retry the job."
        ],
        "human_review_required": true
    }
    """

    with pytest.raises(
        IncidentAnalysisError,
        match="Gemini returned an invalid incident analysis",
    ):
        parse_gemini_incident_analysis(raw_response)