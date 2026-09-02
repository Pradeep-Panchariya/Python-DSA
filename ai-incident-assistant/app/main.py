from fastapi import FastAPI
from app.schemas import IncidentRequest, IncidentAnalysisResponse
from app.services.incident_service import analyze_incident
import logging 
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)
from app.config import settings
logger = logging.getLogger(__name__)

app = FastAPI(
    title = settings.app_name,
    version = settings.app_version
)

logger.info("AI Incident Assistant application started")

@app.get("/health")
def health_check():
    return {"status": "AI Incident Assistant is running"}


@app.post('/analyze-incident', response_model=IncidentAnalysisResponse)
def analyze_incident_endpoint(incident : IncidentRequest) -> IncidentAnalysisResponse:
    logger.info(
        "Received incident analysis request: title=%r",
        incident.title,
    )
    

    analysis = analyze_incident(incident)

    logger.info(
        "Incident analysis completed: category=%r priority=%r",
        analysis["category"],
        analysis["suggested_priority"],
    )

    return analysis