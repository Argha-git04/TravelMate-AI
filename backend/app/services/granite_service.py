"""
IBM Granite service — ibm/granite-4-h-small via watsonx.ai.

SDK version  : ibm-watsonx-ai 1.9.1
Endpoint     : https://us-south.ml.cloud.ibm.com
Inference API: ModelInference.chat()  (structured messages, returns dict)

Response shape:
    response["choices"][0]["message"]["content"]  -> str

Timeout: TextChatParameters(time_limit=<ms>)  — SDK param, not a kwarg.
Retries: ModelInference(max_retries=2, delay_time=1.0) — built-in SDK retry.

HTTP errors : ibm_watsonx_ai.wml_client_error.ApiRequestFailure
General     : ibm_watsonx_ai.wml_client_error.WMLClientError

Security rules (strictly enforced):
- Credentials are read from settings — never hardcoded or logged.
- Error messages are sanitized — no URLs, keys, or project IDs leak to clients.
"""
from __future__ import annotations

import json
import logging
import re
import time
from pathlib import Path
from typing import Any

from fastapi import HTTPException

from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.foundation_models.schema import TextChatParameters
from ibm_watsonx_ai.wml_client_error import ApiRequestFailure, WMLClientError

from app.core.config import get_settings

logger = logging.getLogger(__name__)

# Path to prompt template files (relative to this file's package root)
_PROMPTS_DIR = Path(__file__).parent.parent / "prompts"


def _load_prompt(filename: str) -> str:
    """Load a prompt template from the prompts/ directory."""
    path = _PROMPTS_DIR / filename
    return path.read_text(encoding="utf-8")


def _sanitize_error(exc: Exception) -> str:
    """
    Return a safe error message that contains no credentials, URLs, or
    internal project IDs. Always safe to return to HTTP clients.
    """
    msg = str(exc)
    # Redact anything that looks like a UUID/API key
    msg = re.sub(r"[a-f0-9\-]{20,}", "***", msg)
    # Redact URLs
    msg = re.sub(r"https?://\S+", "[url]", msg)
    # Truncate
    return msg[:200]


def _extract_content(response: dict) -> str:
    """Extract the text content from a chat() response dict."""
    try:
        return response["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as exc:
        logger.error("Unexpected Granite response structure: %s", type(response))
        raise ValueError(f"Unexpected response structure from Granite: {exc}") from exc


def _parse_json_response(text: str, context: str) -> dict | list:
    """
    Extract and parse JSON from the model's text output.
    Granite sometimes wraps JSON in markdown fences — strip them first.
    """
    # Strip markdown code fences if present
    text = text.strip()
    if text.startswith("```"):
        # Remove opening fence (```json or ```)
        text = re.sub(r"^```(?:json)?\s*", "", text)
        # Remove closing fence
        text = re.sub(r"\s*```$", "", text)
        text = text.strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        logger.warning("JSON parse failed for %s. Raw (first 300): %s", context, text[:300])
        raise ValueError(
            f"AI did not return valid JSON for {context}. "
            "Please try again — the model occasionally produces malformed output."
        ) from exc


class GraniteService:
    """
    Thin wrapper around ibm-watsonx-ai ModelInference for TravelMate-AI.

    Instantiated once per request via _get_service() to keep credentials
    out of module-level state, while caching the instance for performance.
    """

    def __init__(self) -> None:
        settings = get_settings()

        # ── Credential validation ──────────────────────────────────────
        missing = []
        if not settings.watsonx_api_key:
            missing.append("WATSONX_API_KEY")
        if not settings.watsonx_project_id:
            missing.append("WATSONX_PROJECT_ID")
        if missing:
            raise HTTPException(
                status_code=503,
                detail=(
                    f"IBM watsonx.ai credentials not configured: {', '.join(missing)}. "
                    "Set them in your backend .env file or Render environment variables."
                ),
            )

        credentials = Credentials(
            url=settings.watsonx_url,
            api_key=settings.watsonx_api_key,
        )

        # validate=False avoids a network call to verify model existence at init.
        # max_retries=2 / delay_time=1.0 — SDK built-in retry on transient failures.
        self._model = ModelInference(
            model_id=settings.granite_model_id,
            credentials=credentials,
            project_id=settings.watsonx_project_id,
            validate=False,
            max_retries=2,
            delay_time=1.0,
        )

        # Default inference params — time_limit is in milliseconds
        self._default_params = TextChatParameters(
            max_tokens=2048,
            temperature=0.3,       # Lower = more deterministic / structured JSON
            repetition_penalty=1.1,
            time_limit=60_000,     # 60 s hard limit at the IBM API level
        )

        logger.info(
            "GraniteService initialised. model=%s project=***",
            settings.granite_model_id,
        )

    # ── Core inference ─────────────────────────────────────────────────

    def _chat(self, system_prompt: str, user_prompt: str) -> str:
        """
        Call ModelInference.chat() with a system + user message pair.
        Returns the raw text content from the response.
        Raises HTTPException on all failure modes.
        """
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_prompt},
        ]

        try:
            t0 = time.monotonic()
            response = self._model.chat(
                messages=messages,
                params=self._default_params,
            )
            elapsed = time.monotonic() - t0
            logger.info("Granite response received in %.2fs", elapsed)
            return _extract_content(response)

        except ApiRequestFailure as exc:
            status = getattr(exc, "status_code", None)
            safe_msg = _sanitize_error(exc)
            logger.error("IBM API error status=%s msg=%s", status, safe_msg)
            if status == 429:
                raise HTTPException(
                    status_code=429,
                    detail="IBM watsonx.ai rate limit reached. Please wait a moment and try again.",
                ) from exc
            if status and 400 <= status < 500:
                raise HTTPException(
                    status_code=502,
                    detail=f"IBM watsonx.ai returned a client error ({status}). {safe_msg}",
                ) from exc
            raise HTTPException(
                status_code=502,
                detail=f"IBM watsonx.ai API error. {safe_msg}",
            ) from exc

        except WMLClientError as exc:
            safe_msg = _sanitize_error(exc)
            logger.error("WMLClientError: %s", safe_msg)
            # Detect timeout by message content (SDK raises WMLClientError on timeout)
            if "timeout" in str(exc).lower() or "timed out" in str(exc).lower():
                raise HTTPException(
                    status_code=504,
                    detail="IBM watsonx.ai request timed out. Please try again.",
                ) from exc
            raise HTTPException(
                status_code=502,
                detail=f"IBM watsonx.ai error: {safe_msg}",
            ) from exc

        except Exception as exc:
            safe_msg = _sanitize_error(exc)
            logger.error("Unexpected Granite error: %s: %s", type(exc).__name__, safe_msg)
            raise HTTPException(
                status_code=500,
                detail="Unexpected error communicating with AI service. Please try again.",
            ) from exc

    # ── Itinerary generation ───────────────────────────────────────────

    def generate_itinerary(
        self,
        destination: str,
        days: int,
        budget_usd: float,
        interests: list[str],
        start_date: str | None,
        travel_style: str,
    ) -> dict:
        """Generate a full day-by-day travel itinerary. Returns parsed JSON dict."""
        system_prompt = _load_prompt("itinerary_prompt.txt")
        user_prompt = (
            f"Generate a {days}-day travel itinerary for {destination}.\n"
            f"Total budget: approximately ${budget_usd:.0f} USD.\n"
            f"Travel style: {travel_style}.\n"
            f"Interests: {', '.join(interests)}.\n"
        )
        if start_date:
            user_prompt += f"Start date: {start_date}.\n"
        user_prompt += "\nRespond with valid JSON only. No explanation outside the JSON."

        raw = self._chat(system_prompt, user_prompt)
        return _parse_json_response(raw, "itinerary")

    # ── Destination recommendations ────────────────────────────────────

    def generate_recommendations(
        self,
        interests: list[str],
        budget_usd: float,
        days: int,
    ) -> list:
        """Generate destination recommendations. Returns parsed JSON list."""
        system_prompt = _load_prompt("recommendation_prompt.txt")
        user_prompt = (
            f"Recommend 5 travel destinations.\n"
            f"Interests: {', '.join(interests)}.\n"
            f"Budget: approximately ${budget_usd:.0f} USD total.\n"
            f"Trip duration: {days} days.\n"
            "\nRespond with a valid JSON array only. No explanation outside the JSON."
        )

        raw = self._chat(system_prompt, user_prompt)
        result = _parse_json_response(raw, "recommendations")
        if not isinstance(result, list):
            raise HTTPException(
                status_code=502,
                detail="AI returned an unexpected format for recommendations. Please try again.",
            )
        return result

    # ── Budget estimation ──────────────────────────────────────────────

    def estimate_budget(
        self,
        destination: str,
        days: int,
        travel_style: str,
    ) -> dict:
        """Estimate trip budget. Returns parsed JSON dict."""
        system_prompt = _load_prompt("budget_prompt.txt")
        user_prompt = (
            f"Estimate the total cost for a trip to {destination} for {days} days.\n"
            f"Travel style: {travel_style}.\n"
            "\nRespond with valid JSON only. No explanation outside the JSON."
        )

        raw = self._chat(system_prompt, user_prompt)
        return _parse_json_response(raw, "budget")


# ── Module-level singleton helper ──────────────────────────────────────────

def get_granite_service() -> GraniteService:
    """
    FastAPI dependency — creates a GraniteService instance per request.
    Raises HTTP 503 immediately if credentials are absent.
    """
    return GraniteService()
