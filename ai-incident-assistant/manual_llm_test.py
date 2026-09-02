from app.services.llm_service import generate_text, LLMServiceError

prompt = (
    "Reply in exactly one sentence."
    "What is the purpose of the health check endpoint?"
)

try:
    print("Sending request to Gemini...")
    response_text = generate_text(prompt)
    print("Received response from Gemini:")
    print(response_text)
except LLMServiceError as error:
    print("LLM request failed : ", error)
