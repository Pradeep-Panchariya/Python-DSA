from app.schemas import IncidentRequest, IncidentAnalysisResponse
import json 
from pydantic import ValidationError

from app.services.llm_service import generate_structured_incident_analysis
from app.services.prompt_service import build_incident_analysis_prompt

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


def analyze_incident_with_gemini(
    incident: IncidentRequest,
) -> IncidentAnalysisResponse:
    prompt = build_incident_analysis_prompt(incident)

    gemini_analysis = generate_structured_incident_analysis(
        prompt
    )

    return IncidentAnalysisResponse(
        **gemini_analysis.model_dump(),
        source="gemini",
    )

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