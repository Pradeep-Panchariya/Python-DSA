from sqlalchemy.orm import session
from app.models import IncidentRecord
from app.schemas import IncidentAnalysisResponse, IncidentRequest
from sqlalchemy.orm import Session

def create_incident_record(
        db: session, 
        incident : IncidentRequest, 
        analysis : IncidentAnalysisResponse,
) -> IncidentRecord:

    incident_record = IncidentRecord(
                title=incident.title,
                description=incident.description,
                summary=analysis.summary,
                category=analysis.category,
                suggested_priority=analysis.suggested_priority,
                investigation_steps=analysis.investigation_steps,
                human_review_required=analysis.human_review_required,
                source=analysis.source,
            )

    db.add(incident_record)
    db.commit()
    db.refresh(incident_record)

    return incident_record

def get_incident_record(
        db: Session, 
        incident_id : int, 
) -> IncidentRecord | None:
    return db.get(IncidentRecord, incident_id)