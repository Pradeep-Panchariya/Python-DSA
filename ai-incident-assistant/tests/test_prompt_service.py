from app.services.prompt_service import build_incident_analysis_prompt
from app.schemas import IncidentRequest

def test_build_incident_analysis_prompt_contains_incident_details():

    incident = IncidentRequest(
        title = "Monthly report email failed",
        description=(
            "Cloud Scheduler completed successfully, but the report "
            "email was not delivered because SMTP authentication failed."
        ),
    )

    prompt = build_incident_analysis_prompt(incident)

    assert "Monthly report email failed" in prompt
    assert "SMTP authentication failed" in prompt
    assert "return ONLY valid JSON" in prompt
    assert '"human_review_required": true' in prompt
    assert "needs_review" in prompt
    assert "P1" in prompt