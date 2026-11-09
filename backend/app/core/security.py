"""
CORS and security middleware configuration.

CORS origins are read from the CORS_ORIGINS environment variable,
never hardcoded. This ensures:
- Local dev:   allows http://localhost:5173
- Production:  allows only the deployed Vercel URL
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings


def configure_cors(app: FastAPI) -> None:
    """Attach CORS middleware to the FastAPI application."""
    settings = get_settings()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["GET", "POST", "DELETE", "OPTIONS"],
        allow_headers=["Content-Type", "Authorization"],
    )
