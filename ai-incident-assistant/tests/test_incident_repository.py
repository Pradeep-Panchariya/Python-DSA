from app.database import SessionLocal
from app.init_db import initialize_database
from app.repositories.incident_repository import create_incident_record, get_incident_record, review_incident_record, list_incident_records
from app.schemas import IncidentAnalysisResponse, IncidentRequest, IncidentReviewRequest


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

def test_get_incident_record_returns_saved_record():
    initialize_database()

    incident = IncidentRequest(
        title="GCP bucket access denied",
        description=(
            "The scheduled process cannot read the input file because "
            "the service account receives a permission denied error."
        ),
    )

    analysis = IncidentAnalysisResponse(
        summary="Service account cannot access the input file.",
        category="access",
        suggested_priority="P2",
        investigation_steps=[
            "Review IAM roles.",
            "Verify bucket permissions.",
            "Check recent policy changes.",
        ],
        human_review_required=True,
        source="gemini",
    )

    db = SessionLocal()
    record = None

    try:
        created_record = create_incident_record(
            db=db,
            incident=incident,
            analysis=analysis,
        )

        record = get_incident_record(
            db=db,
            incident_id=created_record.id,
        )

        assert record is not None
        assert record.id == created_record.id
        assert record.title == "GCP bucket access denied"
        assert record.category == "access"
        assert record.source == "gemini"
    finally:
        if record is not None:
            db.delete(record)
            db.commit()

        db.close()

def test_review_incident_record_updates_saved_record():
    initialize_database()

    incident = IncidentRequest(
        title="Monthly report email failed",
        description=(
            "Cloud Scheduler completed successfully, but the report "
            "email was not delivered because SMTP authentication failed."
        ),
    )

    analysis = IncidentAnalysisResponse(
        summary="Report delivery failed because SMTP authentication failed.",
        category="reporting",
        suggested_priority="P3",
        investigation_steps=[
            "Check SMTP credentials.",
            "Review application logs.",
            "Test the SMTP connection.",
        ],
        human_review_required=True,
        source="gemini",
    )

    review = IncidentReviewRequest(
        reviewed_by="pradeep@example.com",
        review_notes="Confirmed that SMTP credentials were expired.",
        category="reporting",
        suggested_priority="P2",
    )

    db = SessionLocal()
    record = None

    try:
        created_record = create_incident_record(
            db=db,
            incident=incident,
            analysis=analysis,
        )

        record = review_incident_record(
            db=db,
            incident_id=created_record.id,
            review=review,
        )

        assert record is not None
        assert record.reviewed is True
        assert record.reviewed_by == "pradeep@example.com"
        assert record.review_notes == (
            "Confirmed that SMTP credentials were expired."
        )
        assert record.category == "reporting"
        assert record.suggested_priority == "P2"
        assert record.reviewed_at is not None

    finally:
        if record is not None:
            db.delete(record)
            db.commit()

        db.close()

def test_list_incident_records_returns_saved_records():
    initialize_database()

    incident = IncidentRequest(
        title="GCP bucket access denied",
        description=(
            "The scheduled process cannot read the input file because "
            "the service account receives a permission denied error."
        ),
    )

    analysis = IncidentAnalysisResponse(
        summary="Service account cannot access the input file.",
        category="access",
        suggested_priority="P2",
        investigation_steps=[
            "Review IAM roles.",
            "Verify bucket permissions.",
            "Check recent policy changes.",
        ],
        human_review_required=True,
        source="gemini",
    )

    db = SessionLocal()
    created_record = None

    try:
        created_record = create_incident_record(
            db=db,
            incident=incident,
            analysis=analysis,
        )

        records = list_incident_records(
            db=db,
            limit=10,
        )

        record_ids = [record.id for record in records]

        assert created_record.id in record_ids

    finally:
        if created_record is not None:
            db.delete(created_record)
            db.commit()

        db.close()