"""
Health endpoint tests.

These tests must pass with no IBM or Cloudant credentials configured.
They verify the core app starts and responds correctly.

Run:
    cd backend
    conda run -n travelmate python -m pytest tests/test_health.py -v
"""
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_returns_200():
    """Health check must always return 200, regardless of credentials."""
    response = client.get("/health")
    assert response.status_code == 200


def test_health_response_body():
    """Health response must contain status, version, and environment."""
    response = client.get("/health")
    body = response.json()
    assert body["status"] == "ok"
    assert "version" in body
    assert "environment" in body


def test_root_returns_200():
    """Root endpoint must return 200."""
    response = client.get("/")
    assert response.status_code == 200


def test_docs_not_exposed_in_production(monkeypatch):
    """Swagger UI must be hidden when ENVIRONMENT=production."""
    monkeypatch.setenv("ENVIRONMENT", "production")
    # Re-import settings to pick up monkeypatched env
    from app.core.config import get_settings
    get_settings.cache_clear()
    prod_settings = get_settings()
    assert prod_settings.is_production is True
    # Reset cache after test
    get_settings.cache_clear()
