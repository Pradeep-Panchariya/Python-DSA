from pydantic import BaseModel, Field
from typing import Literal

class IncidentRequest(BaseModel):

    title : str = Field(
        min_length=5,
        max_length=150,
        examples=['Monthly report email failed'],
    )

    description : str = Field(
        min_length=10,
        max_length=2000,
        examples = [
            "Cloud schedular was ran successfully, but the report email was not delieverd."
        ]
    )


class IncidentAnalysisResponse(BaseModel):
    summary : str
    category : Literal[
        "reporting",
        "access",
        "platform",
        "backend",
        "data",
        "needs_review",
    ]
    suggested_priority : Literal["P1","P2","P3","P4"]
    investigation_steps : list[str]
    human_review_required : bool 