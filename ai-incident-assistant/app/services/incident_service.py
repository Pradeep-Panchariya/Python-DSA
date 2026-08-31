from app.schemas import IncidentRequest

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
    }