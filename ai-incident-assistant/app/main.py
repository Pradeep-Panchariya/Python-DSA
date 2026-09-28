from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import JSONResponse
from app.services.llm_service import LLMServiceError
from app.schemas import IncidentRequest, IncidentAnalysisResponse, IncidentReviewRequest, IncidentReviewResponse
from app.services.incident_service import analyze_incident_with_gemini
import logging 
from app.init_db import initialize_database
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.repositories.incident_repository import create_incident_record, get_incident_record, review_incident_record, list_incident_records
import uuid 
from app.config import settings

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


@app.get("/config")
def get_public_config():
    return {
        "app_name": settings.app_name,
        "app_version": settings.app_version,
        "environment": settings.environment,
        "gemini_model": settings.gemini_model,
        "gemini_timeout_seconds": settings.gemini_timeout_seconds,
        "database_url_configured": bool(settings.database_url),
        "gemini_api_key_configured": bool(settings.gemini_api_key),
    }

@app.get(
    "/incidents",
    response_model=list[IncidentAnalysisResponse],
)
def list_incidents_endpoint(
    request: Request,
    db: Session = Depends(get_db),
    limit: int = 20,
    reviewed: bool | None = None,
) -> list[IncidentAnalysisResponse]:
    records = list_incident_records(
        db=db,
        limit=limit,
        reviewed=reviewed,
    )

    logger.info(
        "Incident records listed: request_id=%r count=%r reviewed=%r",
        request.state.request_id,
        len(records),
        reviewed,
    )

    return [
        IncidentAnalysisResponse(
            incident_id=record.id,
            summary=record.summary,
            category=record.category,
            suggested_priority=record.suggested_priority,
            investigation_steps=record.investigation_steps,
            human_review_required=record.human_review_required,
            source=record.source,
        )
        for record in records
    ]


@app.get("/incidents/{incident_id}",
         response_model=IncidentAnalysisResponse,
        )
def get_incident_endpoint(
    incident_id : int, 
    request : Request,
    db: Session = Depends(get_db),
) -> IncidentAnalysisResponse:
    record = get_incident_record(db=db, incident_id=incident_id,)

    if record is None:
        raise HTTPException(
            status_code=404,
            detail=f"Incident with id {incident_id} was not found.",
        )

    logger.info(
        "Incident record retrieved: request_id=%r incident_id=%r",
        request.state.request_id,
        record.id,
    )

    return IncidentAnalysisResponse(
        incident_id=record.id,
        summary=record.summary,
        category=record.category,
        suggested_priority=record.suggested_priority,
        investigation_steps=record.investigation_steps,
        human_review_required=record.human_review_required,
        source=record.source,
    )

@app.patch(
    "/incidents/{incident_id}/review",
    response_model=IncidentReviewResponse,
)
def review_incident_endpoint(
    incident_id: int,
    review: IncidentReviewRequest,
    request: Request,
    db: Session = Depends(get_db),
) -> IncidentReviewResponse:
    record = review_incident_record(
        db=db,
        incident_id=incident_id,
        review=review,
    )

    if record is None:
        raise HTTPException(
            status_code=404,
            detail=f"Incident with id {incident_id} was not found.",
        )

    logger.info(
        "Incident reviewed: request_id=%r incident_id=%r reviewed_by=%r",
        request.state.request_id,
        record.id,
        record.reviewed_by,
    )

    return IncidentReviewResponse(
        incident_id=record.id,
        reviewed=record.reviewed,
        reviewed_by=record.reviewed_by,
        review_notes=record.review_notes,
        category=record.category,
        suggested_priority=record.suggested_priority,
    )