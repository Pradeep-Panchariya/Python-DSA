from fastapi import FastAPI
from app.schemas import IncidentRequest, IncidentAnalysisResponse
from app.services.incident_service import analyze_incident


app = FastAPI(
    title = "AI Incident Assistant",
    version = "0.1.0",
)

@app.get("/health")
def health_check():
    return {"status": "AI Incident Assistant is running"}


@app.post('/analyze-incident', response_model=IncidentAnalysisResponse)
def analyze_incident_endpoint(incident : IncidentRequest) -> IncidentAnalysisResponse:
    return analyze_incident(incident)