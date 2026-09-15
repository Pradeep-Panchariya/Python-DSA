from app.schemas import IncidentRequest, IncidentAnalysisResponse
import json 
from pydantic import ValidationError

class IncidentAnalysisError(Exception):
    """Raised when an incident analysis cannot be parsed or validated."""

def analyze_incident(incident: IncidentRequest) -> dict:
    return {
        "summary": (
            f"Incident received: {incident.title}. "
            f"Description: {incident.description}"
        ),
        "category": "needs_review",
        "suggested_priority": "P3",
        "investigation_steps": [
            "Review application logs",
            "Confirm the affected service",
            "Check recent configuration changes",
        ],
        "human_review_required": True,
        "source": "rule_based",
    }

def parse_gemini_incident_analysis(raw_response:str,) -> IncidentAnalysisResponse:
    try: 
        analysis_data = json.loads(raw_response)
    except json.JSONDecodeError as error:
        raise IncidentAnalysisError(
            "Gemini returned invalid JSON."
        ) from error

    analysis_data["source"] = "gemini"

    try:
        return IncidentAnalysisResponse.model_validate(analysis_data)
    except ValidationError as error:
         raise IncidentAnalysisError(
            f"Gemini returned an invalid incident analysis: {error}"
        ) from error