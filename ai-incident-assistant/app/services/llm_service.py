from google import genai
from app.config import settings
from google.genai import types
from pydantic import ValidationError
import time, logging

from app.schemas import GeminiIncidentAnalysis

logger = logging.getLogger(__name__)

class LLMServiceError(Exception):
    """Raised when the LLM service cannot complete a request."""


def generate_text(prompt : str) -> str:
    if not settings.gemini_api_key:
        raise LLMServiceError(
            "GEMINI_API_KEY is not configured. "
            "Add it to your local .env file."
        )

    client = genai.Client(
        api_key = settings.gemini_api_key,
        http_options=types.HttpOptions(timeout=30_000)
        )
    try:
        response = client.interactions.create(
            model = settings.gemini_model,
            input = prompt,
        )

    except Exception as error:
        raise LLMServiceError(
            f"Gemini request failed: {error}"
        ) from error


    if not response.output_text:
        raise LLMServiceError(
            'Gemini returned no text content.'
        )

    return response.output_text



def generate_structured_incident_analysis(
    prompt: str,
) -> GeminiIncidentAnalysis:
    if not settings.gemini_api_key:
        raise LLMServiceError(
            "GEMINI_API_KEY is not configured. "
            "Add it to your local .env file."
        )

    client = client = genai.Client(
                                api_key=settings.gemini_api_key,
                                http_options=types.HttpOptions(
                                    timeout=settings.gemini_timeout_seconds * 1_000,
                                ),
                    )

    start_time = time.perf_counter()

    logger.info(
                "Sending structured Gemini request: model=%r timeout_seconds=%r",
                settings.gemini_model,
                settings.gemini_timeout_seconds,
        )

    try:
        response = client.interactions.create(
            model=settings.gemini_model,
            input=prompt,
            response_format={
                "type": "text",
                "mime_type": "application/json",
                "schema": GeminiIncidentAnalysis.model_json_schema(),
            },
        )
        elapsed_seconds = time.perf_counter() - start_time

        logger.info(
                    "Structured Gemini request completed: duration_seconds=%.2f",
                    elapsed_seconds,
                )
    except Exception as error:
        raise LLMServiceError(
            f"Gemini structured request failed: {error}"
        ) from error

    if not response.output_text:
        raise LLMServiceError(
            "Gemini returned no structured text content."
        )

    try:
        return GeminiIncidentAnalysis.model_validate_json(
            response.output_text
        )
    except ValidationError as error:
        raise LLMServiceError(
            f"Gemini returned invalid structured output: {error}"
        ) from error