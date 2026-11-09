"""
pytest conftest.py — loads backend/.env before any test is collected.

This ensures os.getenv() calls (used by live test skip markers) see the
credentials from .env, not just system environment variables.

Without this, live tests would always show as SKIPPED even when .env is
populated, because pytest collects tests (and evaluates skipif markers)
before the FastAPI app imports pydantic_settings.
"""
import os
from pathlib import Path

# Load .env from the backend directory (where pytest is run from)
env_file = Path(__file__).parent / ".env"
if env_file.exists():
    from dotenv import load_dotenv
    load_dotenv(env_file, override=False)  # Don't override real system env vars

    # Clear the lru_cache so that subsequent get_settings() calls pick up
    # the freshly loaded env vars instead of a cached empty-credentials instance.
    try:
        from app.core.config import get_settings
        get_settings.cache_clear()
    except Exception:
        pass  # If app hasn't been imported yet, nothing to clear
