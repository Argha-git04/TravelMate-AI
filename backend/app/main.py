"""
TravelMate-AI — FastAPI application entry point.

Start locally:
    cd backend
    uvicorn app.main:app --reload --port 8000

API docs (local): http://localhost:8000/docs
Health check:     http://localhost:8000/health
"""
from fastapi import FastAPI

from app.core.config import get_settings
from app.core.security import configure_cors
from app.models.common import HealthResponse
from app.api.v1 import ai, chat, itinerary, weather, maps

settings = get_settings()

app = FastAPI(
    title=settings.app_title,
    version=settings.app_version,
    docs_url="/docs" if not settings.is_production else None,   # Hide docs in production
    redoc_url="/redoc" if not settings.is_production else None,
)

# ── Middleware ────────────────────────────────────────────────
configure_cors(app)

# ── Routers ───────────────────────────────────────────────────
API_PREFIX = "/api/v1"
app.include_router(ai.router,          prefix=API_PREFIX)
app.include_router(chat.router,        prefix=API_PREFIX)
app.include_router(itinerary.router,   prefix=API_PREFIX)
app.include_router(weather.router,     prefix=API_PREFIX)
app.include_router(maps.router,        prefix=API_PREFIX)


# ── Health check ─────────────────────────────────────────────
@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check() -> HealthResponse:
    """
    Always returns 200 OK.
    Intentionally does NOT depend on IBM or Cloudant credentials.
    This endpoint is used by Render to verify the service is running.
    """
    return HealthResponse(
        status="ok",
        version=settings.app_version,
        environment=settings.environment,
    )


@app.get("/", tags=["Health"])
async def root():
    """Redirect hint for the API root."""
    return {"message": "TravelMate-AI API is running. Visit /docs for API documentation."}
