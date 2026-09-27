from app.models import IncidentRecord

def test_incident_record_has_expected_table_name():
    assert IncidentRecord.__tablename__ == 'incidents'

def test_incident_record_has_expected_columns():
    column_names = {
        column.name
        for column in IncidentRecord.__table__.columns
    }

    expected_columns = {
        "id",
        "title",
        "description",
        "summary",
        "category",
        "suggested_priority",
        "investigation_steps",
        "human_review_required",
        "source",
        "created_at",
    }

    assert column_names == expected_columns