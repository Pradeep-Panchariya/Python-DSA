from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.services.llm_service import LLMServiceError
from app.schemas import IncidentRequest, IncidentAnalysisResponse
from app.services.incident_service import analyze_incident_with_gemini
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

@app.exception_handler(LLMServiceError)
def handle_llm_service_error(
    request : Request,
    error : LLMServiceError,
) -> JSONResponse :
    logger.error(
        "LLM service failure: path=%r error=%r",
        request.url.path,
        str(error),
    )

    return JSONResponse(
        status_code=502,
        content={
            "detail":"AI analysis service is temporarily unavailable."
        },
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
    

    analysis = analyze_incident_with_gemini(incident)

    logger.info(
        "Incident analysis completed: category=%r priority=%r",
        analysis.category,
        analysis.suggested_priority,
    )

    return analysis