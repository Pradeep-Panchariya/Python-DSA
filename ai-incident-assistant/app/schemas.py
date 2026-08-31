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