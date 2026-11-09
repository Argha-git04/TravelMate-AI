"""
IBM Granite connectivity test.

Skipped automatically if WATSONX_API_KEY is not set in the environment.
Only runs when credentials are available (CI/CD or local with .env).

Run:
    cd backend
    conda run -n travelmate python -m pytest tests/test_granite.py -v
"""
import os
import pytest

# Skip the entire module if credentials are absent
watsonx_key = os.getenv("WATSONX_API_KEY", "")
pytestmark = pytest.mark.skipif(
    not watsonx_key,
    reason="WATSONX_API_KEY not set — skipping Granite connectivity test",
)


def test_granite_credentials_are_set():
    """Verify all required watsonx.ai env vars are present."""
    assert os.getenv("WATSONX_API_KEY"), "WATSONX_API_KEY must be set"
    assert os.getenv("WATSONX_PROJECT_ID"), "WATSONX_PROJECT_ID must be set"
    assert os.getenv("WATSONX_URL"), "WATSONX_URL must be set"


# TODO Phase 4: add test_granite_generates_text()
#   - instantiate GraniteService
#   - call generate() with a simple prompt
#   - assert response is a non-empty string
