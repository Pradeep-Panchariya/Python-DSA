from app.database import SessionLocal
from app.init_db import initialize_database
from app.repositories.incident_repository import create_incident_record
from app.schemas import IncidentAnalysisResponse, IncidentRequest

def test_create_incident_record():
    initialize_database()

    incident = IncidentRequest(
        title="GCP bucket access denied",
        description=(
            "The scheduled process cannot read the input file because "
            "the service account receives a permission denied error."
        ),
    )

    analysis = IncidentAnalysisResponse(
        summary=(
            "The service account cannot access the input file due to "
            "missing bucket permissions."
        ),
        category="access",
        suggested_priority="P2",
        investigation_steps=[
            "Review service account IAM roles.",
            "Verify bucket-level permissions.",
            "Check recent IAM policy changes.",
        ],
        human_review_required=True,
        source="gemini",
    )

    db = SessionLocal()

    try:
        record = create_incident_record(
            db=db,
            incident=incident,
            analysis=analysis,
        )

        assert record.id is not None
        assert record.title == "GCP bucket access denied"
        assert record.category == "access"
        assert record.suggested_priority == "P2"
        assert record.source == "gemini"
        assert len(record.investigation_steps) == 3
        assert record.created_at is not None
    finally:
        db.delete(record)
        db.commit()
        db.close()