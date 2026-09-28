import pytest
from pydantic import ValidationError

from app.schemas import IncidentReviewRequest

def test_incident_review_request_rejects_invalid_priority():
    with pytest.raises(ValidationError):
        IncidentReviewRequest(
            reviewed_by="pradeep@example.com",
            review_notes="Confirmed that SMTP credentials were expired.",
            category="reporting",
            suggested_priority="P9",
        )