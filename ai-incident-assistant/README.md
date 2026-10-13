# AI Incident Assistant

A production-style FastAPI application that analyzes operational incidents using Google Gemini, validates structured AI output, stores analysis records, and supports human review of AI recommendations.

## Problem

Production-support teams receive incidents involving reporting, access, platform, backend, and data issues. Manual triage can be slow and inconsistent.

AI Incident Assistant accepts an incident title and description, generates a structured triage recommendation using Gemini, stores the result, and allows a human reviewer to approve or override the category and suggested priority.

## Features

- FastAPI REST API with automatically generated Swagger documentation
- Pydantic request and response validation
- Gemini-powered structured incident analysis
- Strict allowed categories and priorities
- Safe LLM error handling with controlled `502 Bad Gateway` responses
- SQLite persistence for local development
- Incident retrieval, listing, and filtering
- Human review workflow for AI-generated recommendations
- Request ID tracing and application logging
- Unit, API, repository, mock, and integration-style tests
- Docker containerization
- Google Cloud Run deployment
- Google Artifact Registry image storage
- Google Secret Manager integration for Gemini API key
- GitHub Actions CI test workflow

## Architecture

mermaid
flowchart TD
Client[Swagger / Frontend / API Client] --> API[FastAPI API]
API --> Validation[Pydantic Validation]
Validation --> IncidentService[Incident Service]
IncidentService --> PromptService[Prompt Service]
PromptService --> LLMService[Gemini LLM Service]
LLMService --> Gemini[Google Gemini API]
Gemini --> LLMService
IncidentService --> Repository[Incident Repository]
Repository --> Database[(SQLite Database)]
API --> Client


## Request Flow

text
POST /analyze-incident
↓
Validate IncidentRequest
↓
Build structured Gemini prompt
↓
Call Gemini Interactions API
↓
Validate Gemini JSON with Pydantic
↓
Store incident and analysis
↓
Return incident ID and structured analysis


## Tech Stack

| Area | Technology |
|---|---|
| Language | Python 3.13 |
| API framework | FastAPI |
| Validation | Pydantic |
| AI provider | Google Gemini API |
| Database | SQLite with SQLAlchemy |
| Testing | pytest, FastAPI TestClient, unittest.mock |
| Containerization | Docker |
| Cloud deployment | Google Cloud Run |
| Image registry | Google Artifact Registry |
| Secrets | Google Secret Manager |
| CI | GitHub Actions |

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/health` | Checks API health |
| `GET` | `/config` | Displays safe non-secret runtime configuration |
| `POST` | `/analyze-incident` | Analyzes and stores an incident |
| `GET` | `/incidents` | Lists incidents with optional filters |
| `GET` | `/incidents/{incident_id}` | Retrieves one incident |
| `PATCH` | `/incidents/{incident_id}/review` | Records human review and optional corrections |

## Local Setup

### 1. Clone the repository

```
bash
git clone https://github.com/Pradeep-Panchariya/Python-DSA.git
cd Python-DSA/ai-incident-assistant
```

### 2. Create and activate a virtual environment

```
bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```
bash
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

```
bash
cp .env.example .env
```

Add your Gemini API key to the local `.env` file:

```
env
APP_NAME=AI Incident Assistant
APP_VERSION=0.1.0
ENVIRONMENT=development
LOG_LEVEL=INFO

GEMINI_API_KEY=your_key_here
GEMINI_MODEL=gemini-3.8-flash
GEMINI_TIMEOUT_SECONDS=60

DATABASE_URL=sqlite:///./incident_assistant.db
```

Never commit `.env`.

### 5. Start the application

```
bash
python -m uvicorn app.main:app --reload
```

Open Swagger UI:

```
text
http://127.0.0.1:8000/docs
```

## Run Tests

```
bash
python -m pytest -v
```

The project includes:

- Unit tests
- FastAPI API/route tests
- Repository tests using SQLite
- Mocked Gemini service tests
- Configuration tests
- Request and response validation tests

Gemini calls are mocked during automated tests, so tests do not use Gemini credits or require an API key.

## Docker

### Build the Docker image

```
bash
docker build -t ai-incident-assistant:local .
```

### Run without Gemini configuration

This is suitable for testing `/health`, `/config`, and Swagger.

```
bash
docker run --rm -p 8080:8080 ai-incident-assistant:local
```

Open:

```
text
http://127.0.0.1:8080/docs
```

### Run with local environment values

```
bash
docker run --rm \
--env-file .env \
-p 8080:8080 \
ai-incident-assistant:local
```

Verify safe configuration:

```
text
http://127.0.0.1:8080/config
```

The response should show:

```
json
{
"gemini_api_key_configured": true
}
```

The actual Gemini API key is never returned by the API.

## Google Cloud Deployment

The application was deployed to Google Cloud Run using this flow:

```
text
Local Docker build
↓
Artifact Registry
↓
Cloud Run
↓
Secret Manager injects GEMINI_API_KEY
```

The Docker image was built for Cloud Run's Linux AMD64 environment:

```
bash
docker buildx build \
--platform linux/amd64 \
--tag <ARTIFACT_REGISTRY_IMAGE_URI> \
--push \
.
```

Example Artifact Registry image format:

```
text
asia-south1-docker.pkg.dev/PROJECT_ID/ai-images/ai-incident-assistant:v1
```

Cloud Run receives runtime configuration through environment variables:

```
text
ENVIRONMENT=production
GEMINI_MODEL=gemini-3.8-flash
GEMINI_TIMEOUT_SECONDS=60
DATABASE_URL=sqlite:////tmp/incident_assistant.db
```

> **Important:** SQLite storage in Cloud Run `/tmp` is temporary. Data can be lost when an instance restarts, scales down, or a different instance handles the request.

A production implementation should replace SQLite with Cloud SQL PostgreSQL or another managed persistent database.

## Security Decisions

- Gemini API key is excluded from Git through `.gitignore`
- `.env` is excluded from Docker images through `.dockerignore`
- Cloud Run receives the Gemini key through Secret Manager
- `/config` returns only whether an API key is configured, never the API key value
- LLM provider errors are logged internally
- API clients receive a safe generic error response for provider failures
- Pydantic schemas validate API input and AI-generated output
- `Literal` types restrict categories and priorities to approved values
- Request IDs are added to logs and API responses for request tracing

## Example Incident Analysis Response

```
json
{
"incident_id": 1,
"summary": "Monthly report email delivery failed due to an SMTP authentication failure after report generation.",
"category": "reporting",
"suggested_priority": "P3",
"investigation_steps": [
  "Verify SMTP credentials and configured secrets.",
  "Review application logs for SMTP authentication errors.",
  "Test SMTP connection using the configured service account."
],
"human_review_required": true,
"source": "gemini"
}
```

## Human Review Workflow

AI-generated analysis should not be treated as a final operational decision.

A reviewer can update an incident through:

```
text
PATCH /incidents/{incident_id}/review
```

The review captures:

- Reviewer identity
- Review notes
- Approved or corrected category
- Approved or corrected priority
- Review timestamp

This implements a human-in-the-loop workflow for safer AI-assisted incident triage.

## CI Pipeline

GitHub Actions runs the test suite automatically whenever code is pushed to the `main` branch.

```
text
git push
↓
GitHub Actions runner starts
↓
Python environment is created
↓
Dependencies are installed
↓
pytest test suite runs
↓
Pass/fail status is displayed in GitHub Actions
```

## Limitations

- Cloud Run SQLite storage is temporary and unsuitable for production persistence
- Gemini response quality depends on incident description quality
- No authentication or role-based access control is currently implemented
- The deployed demo should use synthetic incident data only
- Gemini rate limits or quota limits can return controlled `502` responses
- The application does not yet use RAG or approved runbook retrieval

## Future Improvements

- Replace SQLite with Cloud SQL PostgreSQL
- Add Alembic database migrations
- Add authentication and role-based access control
- Add pagination and sorting to `GET /incidents`
- Add rate limiting
- Add RAG over approved incident runbooks
- Add source citations for AI investigation recommendations
- Add AI evaluation data and quality metrics
- Add GitHub Actions CD pipeline for Cloud Run deployment
- Add OpenTelemetry tracing and Cloud Monitoring alerts
- Deploy the Docker image to Kubernetes/GKE as a separate platform-engineering exercise

## Author

Pradeep Panchariya  
Python, GCP, Backend and Applied AI Engineering Project
```
`