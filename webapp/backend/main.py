"""
PESAMultiCloudIntel — WebApp Backend
=====================================
FastAPI server that proxies natural language questions to the ICA
Workflow API (IBM Consulting Advantage / Langflow) and returns the
AI-generated answer to the React frontend.

Endpoints:
  GET  /            — service info
  GET  /health      — health check
  POST /api/chat    — send a question, receive an AI answer

Start with:
  uvicorn main:app --port 8001 --reload
"""

import logging
import os
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator

from ica_adapter import ICAAdapter, ICAAdapterError, VALID_CLOUD_PROVIDERS

# ---------------------------------------------------------------------------
# Environment
# ---------------------------------------------------------------------------

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# CORS configuration (read once at module load)
# ---------------------------------------------------------------------------

_raw_origins = os.getenv("CORS_ORIGINS", "").strip()
CORS_ORIGINS: list[str] = (
    [o.strip() for o in _raw_origins.split(",") if o.strip()]
    if _raw_origins
    else ["http://localhost:5173"]
)

# ---------------------------------------------------------------------------
# Lifespan — create ICAAdapter once at startup
# ---------------------------------------------------------------------------

_adapter: ICAAdapter | None = None


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    global _adapter

    backend_port = os.getenv("BACKEND_PORT", "8001")

    logger.info("=" * 60)
    logger.info("PESAMultiCloudIntel Backend starting up")
    logger.info("  Port        : %s", backend_port)
    logger.info("  CORS origins: %s", CORS_ORIGINS)
    logger.info("=" * 60)

    _adapter = ICAAdapter()   # raises EnvironmentError if .env is missing
    logger.info("ICAAdapter initialised successfully.")

    yield  # application runs here

    logger.info("PESAMultiCloudIntel Backend shutting down.")
    _adapter = None


# ---------------------------------------------------------------------------
# FastAPI application
# ---------------------------------------------------------------------------

app = FastAPI(
    title="PESAMultiCloudIntel Backend",
    version="1.0.0",
    description="Proxy API between the React chat UI and the ICA Workflow API.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Request / Response models
# ---------------------------------------------------------------------------


class ChatRequest(BaseModel):
    question: str
    cloud_provider: str = "all"

    @field_validator("question")
    @classmethod
    def question_must_not_be_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("question must not be empty")
        return v.strip()

    @field_validator("cloud_provider")
    @classmethod
    def cloud_provider_must_be_valid(cls, v: str) -> str:
        normalised = v.strip().lower()
        if normalised not in VALID_CLOUD_PROVIDERS:
            raise ValueError(
                f"cloud_provider must be one of: "
                f"{', '.join(sorted(VALID_CLOUD_PROVIDERS))}"
            )
        return normalised


class ChatResponse(BaseModel):
    answer: str
    cloud_provider: str


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------


@app.get("/", summary="Service info")
async def root() -> dict[str, Any]:
    """Return basic service metadata."""
    return {
        "name": "PESAMultiCloudIntel Backend",
        "version": "1.0.0",
        "description": "Proxy API for the ICA Workflow (IBM Consulting Advantage).",
        "endpoints": {
            "health": "GET /health",
            "chat":   "POST /api/chat",
        },
    }


@app.get("/health", summary="Health check")
async def health() -> dict[str, str]:
    """Confirm the service is running."""
    return {"status": "ok"}


@app.post("/api/chat", response_model=ChatResponse, summary="Send a question to ICA")
async def chat(request: ChatRequest) -> ChatResponse:
    """
    Send a natural language question to the ICA Workflow API and return
    the AI-generated answer.

    - **question**: Natural language question (must not be empty).
    - **cloud_provider**: One of ``all``, ``aws``, ``azure``, ``gcp``.
      Defaults to ``all``.
    """
    if _adapter is None:
        # Should never happen if lifespan ran correctly
        raise HTTPException(status_code=503, detail="Adapter not initialised.")

    logger.info(
        "Chat request received — cloud_provider=%s question_length=%d",
        request.cloud_provider,
        len(request.question),
    )

    try:
        answer = await _adapter.call(request.question, request.cloud_provider)
    except ICAAdapterError as exc:
        logger.error("ICAAdapterError: %s", exc)
        raise HTTPException(
            status_code=502,
            detail=(
                "The ICA Workflow API returned an error. "
                "Please check your ICA credentials and workflow ID, "
                f"then try again. Detail: {exc}"
            ),
        ) from exc
    except Exception as exc:
        logger.exception("Unexpected error during chat request: %s", exc)
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred. Please try again.",
        ) from exc

    logger.info(
        "Chat response ready — cloud_provider=%s answer_length=%d",
        request.cloud_provider,
        len(answer),
    )
    return ChatResponse(answer=answer, cloud_provider=request.cloud_provider)
