"""
CORS header tests.

Verifies that the backend sends the correct CORS headers so the
React frontend can call the API without browser errors.

Run:
    cd backend
    conda run -n travelmate python -m pytest tests/test_cors.py -v
"""
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_cors_header_present_for_allowed_origin():
    """
    Preflight request from the allowed origin must return
    Access-Control-Allow-Origin header.
    """
    response = client.options(
        "/health",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "GET",
        },
    )
    assert response.status_code in (200, 204)
    assert "access-control-allow-origin" in response.headers


def test_cors_allows_configured_origin():
    """GET request from allowed origin must include CORS header in response."""
    response = client.get(
        "/health",
        headers={"Origin": "http://localhost:5173"},
    )
    assert response.status_code == 200
    assert response.headers.get("access-control-allow-origin") == "http://localhost:5173"
