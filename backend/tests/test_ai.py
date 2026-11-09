"""
AI service unit tests — tests for GraniteService helper functions and
API endpoint behaviour.

All tests run WITHOUT IBM credentials by default, using mocking where needed.

Tests cover:
- JSON parsing (valid, invalid, markdown fences)
- Error sanitization (no credentials leaked)
- Missing credentials → HTTP 503
- Input validation → HTTP 422 (via dependency override)
- API response structure (is_estimated=True on all prices)
- Optional live Granite integration (skipped when creds absent)

Run:
    cd backend
    & "C:\\Users\\argha\\anaconda3\\envs\\travelmate\\python.exe" -m pytest tests/test_ai.py -v
"""
import json
import os
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services.granite_service import (
    _parse_json_response,
    _sanitize_error,
    _extract_content,
    _load_prompt,
)

client = TestClient(app)

# ════════════════════════════════════════════════════════════════
# Helper function unit tests (no network, no credentials)
# ════════════════════════════════════════════════════════════════

class TestParseJsonResponse:
    def test_valid_json_object(self):
        data = {"destination": "Paris", "days": 3}
        result = _parse_json_response(json.dumps(data), "test")
        assert result == data

    def test_valid_json_array(self):
        data = [{"destination": "Paris"}, {"destination": "Tokyo"}]
        result = _parse_json_response(json.dumps(data), "test")
        assert result == data

    def test_strips_markdown_json_fence(self):
        raw = '```json\n{"destination": "Paris"}\n```'
        result = _parse_json_response(raw, "test")
        assert result["destination"] == "Paris"

    def test_strips_plain_code_fence(self):
        raw = '```\n{"destination": "Paris"}\n```'
        result = _parse_json_response(raw, "test")
        assert result["destination"] == "Paris"

    def test_raises_value_error_on_invalid_json(self):
        with pytest.raises(ValueError, match="AI did not return valid JSON"):
            _parse_json_response("this is not json", "test")

    def test_raises_value_error_on_empty_string(self):
        with pytest.raises((ValueError, json.JSONDecodeError)):
            _parse_json_response("", "test")


class TestSanitizeError:
    def test_redacts_uuid_style_strings(self):
        fake_key = "abcdef1234567890abcdef1234567890"
        exc = Exception(f"Error with key {fake_key}")
        result = _sanitize_error(exc)
        assert fake_key not in result
        assert "***" in result

    def test_redacts_urls(self):
        exc = Exception("Failed at https://us-south.ml.cloud.ibm.com/ml/v1/text")
        result = _sanitize_error(exc)
        assert "us-south.ml.cloud.ibm.com" not in result
        assert "[url]" in result

    def test_truncates_long_messages(self):
        exc = Exception("x" * 500)
        result = _sanitize_error(exc)
        assert len(result) <= 200

    def test_safe_message_passthrough(self):
        exc = Exception("Connection refused")
        result = _sanitize_error(exc)
        assert "Connection refused" in result


class TestExtractContent:
    def test_extracts_content_from_valid_response(self):
        response = {"choices": [{"message": {"content": "Hello world"}}]}
        assert _extract_content(response) == "Hello world"

    def test_raises_on_empty_choices(self):
        with pytest.raises(ValueError):
            _extract_content({"choices": []})

    def test_raises_on_missing_choices(self):
        with pytest.raises(ValueError):
            _extract_content({})

    def test_raises_on_none(self):
        with pytest.raises((ValueError, TypeError)):
            _extract_content(None)


class TestLoadPrompt:
    def test_loads_itinerary_prompt(self):
        content = _load_prompt("itinerary_prompt.txt")
        assert len(content) > 50
        assert "itinerary" in content.lower()

    def test_loads_recommendation_prompt(self):
        content = _load_prompt("recommendation_prompt.txt")
        assert len(content) > 50

    def test_loads_budget_prompt(self):
        content = _load_prompt("budget_prompt.txt")
        assert len(content) > 50

    def test_missing_file_raises(self):
        with pytest.raises(FileNotFoundError):
            _load_prompt("nonexistent_prompt.txt")


# ════════════════════════════════════════════════════════════════
# API endpoint tests — missing credentials (no mock needed)
# ════════════════════════════════════════════════════════════════

class TestMissingCredentials:
    """Verifies endpoints return 503 when IBM creds are absent."""

    def test_itinerary_returns_503_when_no_credentials(self):
        resp = client.post("/api/v1/ai/itinerary", json={
            "destination": "Paris, France",
            "days": 3,
            "budget_usd": 1500,
            "interests": ["Food & Cuisine", "Culture & History"],
            "travel_style": "mid-range",
        })
        # 503 = credentials missing; 200 = creds present (live env)
        assert resp.status_code in (503, 200)
        if resp.status_code == 503:
            detail = resp.json()["detail"].lower()
            assert "credentials" in detail or "configured" in detail

    def test_recommend_returns_503_when_no_credentials(self):
        resp = client.post("/api/v1/ai/recommend", json={
            "interests": ["Beach & Relaxation"],
            "budget_usd": 2000,
            "days": 7,
        })
        assert resp.status_code in (503, 200)

    def test_budget_returns_503_when_no_credentials(self):
        resp = client.post("/api/v1/ai/budget", json={
            "destination": "Tokyo, Japan",
            "days": 5,
            "travel_style": "budget",
        })
        assert resp.status_code in (503, 200)

    def test_503_detail_does_not_leak_credential_values(self):
        """The 503 message must name missing variables, not expose their values."""
        resp = client.post("/api/v1/ai/budget", json={
            "destination": "Paris", "days": 3, "travel_style": "budget",
        })
        if resp.status_code == 503:
            text = resp.text
            # The message may mention variable NAMES (e.g. "WATSONX_API_KEY")
            # but must never contain what looks like an actual key value
            # (long hex strings or bearer token patterns)
            import re
            # No bearer-token-length hex strings
            assert not re.search(r"[a-f0-9]{32,}", text, re.IGNORECASE)


# ════════════════════════════════════════════════════════════════
# Mocked endpoint tests — use dependency_overrides correctly
# ════════════════════════════════════════════════════════════════

MOCK_ITINERARY_JSON = {
    "destination": "Paris, France",
    "duration_days": 2,
    "total_estimated_cost_usd": 800,
    "is_estimated": True,
    "days": [
        {
            "day_number": 1,
            "title": "Arrival & Eiffel Tower",
            "activities": [
                {
                    "time": "14:00",
                    "name": "Visit Eiffel Tower",
                    "description": "Iconic landmark",
                    "location_name": "Eiffel Tower",
                    "estimated_cost_usd": 30,
                    "is_estimated": True,
                }
            ],
            "accommodation": {"name": "Hotel Paris", "type": "hotel", "estimated_cost_usd": 120},
            "transport": {"type": "metro", "description": "Metro line 6", "estimated_cost_usd": 10},
            "day_estimated_total_usd": 160,
        }
    ],
}

MOCK_RECOMMEND_JSON = [
    {
        "destination": "Tokyo, Japan",
        "country": "Japan",
        "description": "A fantastic city.",
        "highlights": ["Temples", "Food", "Tech"],
        "best_time_to_visit": "Spring",
        "estimated_total_cost_usd": 2000,
        "difficulty_level": "easy",
    }
]

MOCK_BUDGET_JSON = {
    "destination": "Tokyo, Japan",
    "days": 5,
    "travel_style": "mid-range",
    "breakdown": {
        "accommodation_per_night_usd": 100,
        "food_per_day_usd": 50,
        "transport_total_usd": 80,
        "activities_total_usd": 120,
        "miscellaneous_usd": 50,
    },
    "total_estimated_usd": 980,
    "notes": "Budget may vary.",
}


def _make_mock_service(itinerary=None, recommend=None, budget=None):
    svc = MagicMock()
    if itinerary is not None:
        svc.generate_itinerary.return_value = itinerary
    if recommend is not None:
        svc.generate_recommendations.return_value = recommend
    if budget is not None:
        svc.estimate_budget.return_value = budget
    return svc


class TestMockedEndpoints:
    """Test endpoint response structure using dependency_overrides."""

    def setup_method(self):
        """Ensure overrides are cleared before each test."""
        app.dependency_overrides.clear()

    def teardown_method(self):
        """Always clear overrides after each test."""
        app.dependency_overrides.clear()

    def test_itinerary_response_has_is_estimated_true(self):
        from app.services.granite_service import get_granite_service
        mock_svc = _make_mock_service(itinerary=MOCK_ITINERARY_JSON)
        app.dependency_overrides[get_granite_service] = lambda: mock_svc

        resp = client.post("/api/v1/ai/itinerary", json={
            "destination": "Paris, France", "days": 2,
            "budget_usd": 800, "interests": ["Culture"],
            "travel_style": "mid-range",
        })
        assert resp.status_code == 200, resp.text
        body = resp.json()
        assert body["is_estimated"] is True
        assert body["granite_model"] == "ibm/granite-4-h-small"
        assert len(body["days"]) == 1
        day = body["days"][0]
        assert day["is_estimated"] is True
        assert day["activities"][0]["is_estimated"] is True

    def test_recommend_response_has_is_estimated_true(self):
        from app.services.granite_service import get_granite_service
        mock_svc = _make_mock_service(recommend=MOCK_RECOMMEND_JSON)
        app.dependency_overrides[get_granite_service] = lambda: mock_svc

        resp = client.post("/api/v1/ai/recommend", json={
            "interests": ["Culture"], "budget_usd": 2000, "days": 7,
        })
        assert resp.status_code == 200, resp.text
        body = resp.json()
        assert body["is_estimated"] is True
        assert len(body["recommendations"]) == 1
        assert body["recommendations"][0]["is_estimated"] is True

    def test_budget_response_has_is_estimated_true(self):
        from app.services.granite_service import get_granite_service
        mock_svc = _make_mock_service(budget=MOCK_BUDGET_JSON)
        app.dependency_overrides[get_granite_service] = lambda: mock_svc

        resp = client.post("/api/v1/ai/budget", json={
            "destination": "Tokyo, Japan", "days": 5, "travel_style": "mid-range",
        })
        assert resp.status_code == 200, resp.text
        body = resp.json()
        assert body["is_estimated"] is True
        assert body["total_estimated_usd"] == 980.0
        assert body["breakdown"]["accommodation_per_night_usd"] == 100.0

    def test_itinerary_validates_missing_destination(self):
        """Pydantic validation (422) is tested with a mock service to bypass 503."""
        from app.services.granite_service import get_granite_service
        mock_svc = _make_mock_service(itinerary=MOCK_ITINERARY_JSON)
        app.dependency_overrides[get_granite_service] = lambda: mock_svc

        resp = client.post("/api/v1/ai/itinerary", json={
            "days": 3, "budget_usd": 1000, "interests": ["Food"]
        })
        assert resp.status_code == 422

    def test_itinerary_validates_zero_days(self):
        from app.services.granite_service import get_granite_service
        mock_svc = _make_mock_service(itinerary=MOCK_ITINERARY_JSON)
        app.dependency_overrides[get_granite_service] = lambda: mock_svc

        resp = client.post("/api/v1/ai/itinerary", json={
            "destination": "Paris", "days": 0,
            "budget_usd": 1000, "interests": ["Food"],
        })
        assert resp.status_code == 422

    def test_itinerary_validates_negative_budget(self):
        from app.services.granite_service import get_granite_service
        mock_svc = _make_mock_service(itinerary=MOCK_ITINERARY_JSON)
        app.dependency_overrides[get_granite_service] = lambda: mock_svc

        resp = client.post("/api/v1/ai/itinerary", json={
            "destination": "Paris", "days": 3,
            "budget_usd": -100, "interests": ["Food"],
        })
        assert resp.status_code == 422

    def test_itinerary_validates_invalid_travel_style(self):
        from app.services.granite_service import get_granite_service
        mock_svc = _make_mock_service(itinerary=MOCK_ITINERARY_JSON)
        app.dependency_overrides[get_granite_service] = lambda: mock_svc

        resp = client.post("/api/v1/ai/itinerary", json={
            "destination": "Paris", "days": 3, "budget_usd": 1000,
            "interests": ["Food"], "travel_style": "super-premium",
        })
        assert resp.status_code == 422

    def test_budget_validates_days_over_30(self):
        from app.services.granite_service import get_granite_service
        mock_svc = _make_mock_service(budget=MOCK_BUDGET_JSON)
        app.dependency_overrides[get_granite_service] = lambda: mock_svc

        resp = client.post("/api/v1/ai/budget", json={
            "destination": "Paris", "days": 31, "travel_style": "budget",
        })
        assert resp.status_code == 422


# ════════════════════════════════════════════════════════════════
# Optional live Granite integration test
# ════════════════════════════════════════════════════════════════

watsonx_key = os.getenv("WATSONX_API_KEY", "")
live_mark = pytest.mark.skipif(
    not watsonx_key,
    reason="WATSONX_API_KEY not set — skipping live Granite integration test",
)


@live_mark
def test_granite_live_itinerary_generation():
    """
    Live end-to-end test: calls the real IBM Granite API.
    Only runs when WATSONX_API_KEY is set in the environment.
    """
    resp = client.post("/api/v1/ai/itinerary", json={
        "destination": "Paris, France",
        "days": 2,
        "budget_usd": 1000,
        "interests": ["Culture & History", "Food & Cuisine"],
        "travel_style": "mid-range",
    })
    assert resp.status_code == 200, f"Expected 200, got {resp.status_code}: {resp.text[:300]}"
    body = resp.json()
    assert body["is_estimated"] is True
    assert body["granite_model"] == "ibm/granite-4-h-small"
    assert isinstance(body["days"], list)
    assert len(body["days"]) >= 1


@live_mark
def test_granite_live_budget_estimation():
    """Live budget estimation test."""
    resp = client.post("/api/v1/ai/budget", json={
        "destination": "Tokyo, Japan",
        "days": 5,
        "travel_style": "mid-range",
    })
    assert resp.status_code == 200
    body = resp.json()
    assert body["is_estimated"] is True
    assert body["total_estimated_usd"] > 0
