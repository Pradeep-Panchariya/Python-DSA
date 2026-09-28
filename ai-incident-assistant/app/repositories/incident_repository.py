from sqlalchemy.orm import session
from app.models import IncidentRecord
from app.schemas import IncidentAnalysisResponse, IncidentRequest, IncidentReviewRequest
from sqlalchemy.orm import Session
from datetime import datetime, timezone 

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

def review_incident_record(
    db: Session,
    incident_id: int,
    review: IncidentReviewRequest,
) -> IncidentRecord | None:
    incident_record = db.get(IncidentRecord, incident_id)

    if incident_record is None:
        return None

    incident_record.reviewed = True
    incident_record.reviewed_by = review.reviewed_by
    incident_record.review_notes = review.review_notes
    incident_record.category = review.category
    incident_record.suggested_priority = review.suggested_priority
    incident_record.reviewed_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(incident_record)

    return incident_record