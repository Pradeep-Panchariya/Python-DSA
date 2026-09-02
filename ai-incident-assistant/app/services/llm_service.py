from google import genai
from app.config import settings
from google.genai import types

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