from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse
from app.services.llm_service import LLMServiceError
from app.schemas import IncidentRequest, IncidentAnalysisResponse
from app.services.incident_service import analyze_incident_with_gemini
import logging 
from app.init_db import initialize_database
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.repositories.incident_repository import create_incident_record
import uuid 


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


@app.on_event("startup")
def create_database_table() -> None:
    initialize_database()
    logger.info("Database table initialized")


@app.middleware("http")
async def add_request_id(request : Request, call_next,):

    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()),)

    request.state.request_id = request_id 
    response = await call_next(request)

    response.headers["X-Request-ID"] = request_id

    return response 


@app.exception_handler(LLMServiceError)
def handle_llm_service_error(
    request : Request,
    error : LLMServiceError,
) -> JSONResponse :
    logger.error(
        "LLM service failure: request_id=%r path=%r error=%r",
        request.state.request_id,
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
def analyze_incident_endpoint(incident : IncidentRequest, request : Request, db: Session = Depends(get_db),) -> IncidentAnalysisResponse:
    logger.info(
                "Received incident analysis request: request_id=%r title=%r",
                request.state.request_id,
                incident.title,
            )
    

    analysis = analyze_incident_with_gemini(incident)

    record = create_incident_record(
                db=db,
                incident=incident,
                analysis=analysis,
            )


    logger.info(
                "Incident analysis completed: request_id=%r category=%r priority=%r",
                request.state.request_id,
                analysis.category,
                analysis.suggested_priority,
            )

    logger.info(
            "Incident record saved: request_id=%r incident_id=%r",
            request.state.request_id,
            record.id,  
        )

    return analysis.model_copy(
                    update={"incident_id": record.id}
                )

