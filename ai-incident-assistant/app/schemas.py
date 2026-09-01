from pydantic import BaseModel, Field


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
    category : str 
    suggested_priority : str 
    investigation_steps : list[str]
    human_review_required : bool 