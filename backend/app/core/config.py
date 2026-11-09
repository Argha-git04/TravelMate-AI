"""
Application configuration using Pydantic Settings.

Reads environment variables from the OS environment (production / Render)
or from the backend/.env file (local development).

Design decisions:
- The health check (/health) never depends on IBM or Cloudant credentials.
- IBM and Cloudant credentials are optional strings (default "").
- Each service (granite_service, cloudant_service) validates its own
  required credentials at call-time and raises HTTP 503 if they are absent.
  This means the app always starts successfully; missing creds only surface
  when the relevant endpoint is called.
"""
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # ── IBM watsonx.ai ────────────────────────────────────────
    # Optional at startup — validated by granite_service at call-time
    watsonx_api_key: str = ""
    watsonx_project_id: str = ""
    watsonx_url: str = "https://us-south.ml.cloud.ibm.com"
    granite_model_id: str = "ibm/granite-4-h-small"

    # ── IBM Cloudant ──────────────────────────────────────────
    # Optional at startup — validated by cloudant_service at call-time
    cloudant_url: str = ""
    cloudant_apikey: str = ""
    cloudant_db_itineraries: str = "travelmate_itineraries"
    cloudant_db_chat: str = "travelmate_chat_sessions"

    # ── CORS ──────────────────────────────────────────────────
    # Comma-separated list of allowed frontend origins.
    # Local dev default; override via env var in production.
    cors_origins: str = "http://localhost:5173"

    # ── App ───────────────────────────────────────────────────
    environment: str = "development"
    app_title: str = "TravelMate-AI API"
    app_version: str = "1.0.0"

    model_config = SettingsConfigDict(
        env_file=".env",           # Loaded in local dev; ignored if file absent
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",            # Silently ignore unknown env vars
    )

    @property
    def cors_origins_list(self) -> list[str]:
        """Return CORS_ORIGINS as a Python list."""
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]

    @property
    def is_production(self) -> bool:
        return self.environment.lower() == "production"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """
    Return the cached Settings singleton.
    Using lru_cache means .env is read exactly once at startup.
    """
    return Settings()
