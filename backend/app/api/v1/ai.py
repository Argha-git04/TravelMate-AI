"""
AI endpoints — IBM Granite (ibm/granite-4-h-small) via watsonx.ai.

Routes:
    POST /api/v1/ai/recommend   — destination recommendations
    POST /api/v1/ai/itinerary   — full day-by-day travel itinerary
    POST /api/v1/ai/budget      — trip budget estimation

All endpoints:
- Require valid request body (Pydantic validation, HTTP 422 on failure).
- Return HTTP 503 if IBM credentials are not configured.
- Return HTTP 502/504 on IBM API errors.
- Never expose IBM credentials in responses or logs.
- Tag all AI-generated costs with is_estimated=True.
"""
from __future__ import annotations

import logging
from typing import Any

from fastapi import APIRouter, Depends, HTTPException

from app.models.itinerary import (
    BudgetRequest,
    BudgetResponse,
    BudgetBreakdown,
    ItineraryRequest,
    ItineraryResponse,
    DayPlanResponse,
    ActivityResponse,
    AccommodationResponse,
    TransportResponse,
    RecommendRequest,
    RecommendResponse,
    RecommendationItem,
)
from app.services.granite_service import GraniteService, get_granite_service

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/ai", tags=["AI"])


# ── Helper: safe dict access ───────────────────────────────────────────────

def _safe_float(d: dict, key: str, default: float = 0.0) -> float:
    """Extract a float from a dict, returning default on missing/invalid."""
    try:
        return float(d.get(key, default) or default)
    except (TypeError, ValueError):
        return default


def _safe_str(d: dict, key: str, default: str = "") -> str:
    return str(d.get(key, default) or default)


def _safe_list(d: dict, key: str) -> list:
    v = d.get(key, [])
    return v if isinstance(v, list) else []


# ── /ai/itinerary ──────────────────────────────────────────────────────────

@router.post("/itinerary", response_model=ItineraryResponse)
async def generate_itinerary(
    request: ItineraryRequest,
    service: GraniteService = Depends(get_granite_service),  # 503 if creds missing
) -> ItineraryResponse:
    """
    Generate a personalized day-by-day travel itinerary using IBM Granite.

    All returned cost values are AI estimates (is_estimated=True).
    They are not verified live prices.
    """
    logger.info(
        "itinerary request: destination=%s days=%d budget=%.0f",
        request.destination, request.days, request.budget_usd,
    )

    raw = service.generate_itinerary(
        destination=request.destination,
        days=request.days,
        budget_usd=request.budget_usd,
        interests=request.interests,
        start_date=request.start_date,
        travel_style=request.travel_style,
    )

    # ── Parse days ────────────────────────────────────────────────────
    days_out: list[DayPlanResponse] = []
    for day_raw in _safe_list(raw, "days"):
        if not isinstance(day_raw, dict):
            continue

        activities = [
            ActivityResponse(
                time=_safe_str(act, "time"),
                name=_safe_str(act, "name", "Activity"),
                description=_safe_str(act, "description"),
                location_name=_safe_str(act, "location_name"),
                estimated_cost_usd=_safe_float(act, "estimated_cost_usd"),
                is_estimated=True,
            )
            for act in _safe_list(day_raw, "activities")
            if isinstance(act, dict)
        ]

        acc_raw = day_raw.get("accommodation") or {}
        accommodation = AccommodationResponse(
            name=_safe_str(acc_raw, "name"),
            type=_safe_str(acc_raw, "type"),
            estimated_cost_usd=_safe_float(acc_raw, "estimated_cost_usd"),
            is_estimated=True,
        ) if acc_raw else None

        tr_raw = day_raw.get("transport") or {}
        transport = TransportResponse(
            type=_safe_str(tr_raw, "type"),
            description=_safe_str(tr_raw, "description"),
            estimated_cost_usd=_safe_float(tr_raw, "estimated_cost_usd"),
            is_estimated=True,
        ) if tr_raw else None

        days_out.append(DayPlanResponse(
            day_number=int(day_raw.get("day_number", len(days_out) + 1)),
            title=_safe_str(day_raw, "title"),
            activities=activities,
            accommodation=accommodation,
            transport=transport,
            day_estimated_total_usd=_safe_float(day_raw, "day_estimated_total_usd"),
            is_estimated=True,
        ))

    return ItineraryResponse(
        destination=_safe_str(raw, "destination", request.destination),
        duration_days=int(raw.get("duration_days", request.days)),
        total_estimated_cost_usd=_safe_float(raw, "total_estimated_cost_usd"),
        is_estimated=True,
        days=days_out,
        travel_style=request.travel_style,
        granite_model="ibm/granite-4-h-small",
        raw_ai_data=raw,
    )


# ── /ai/recommend ──────────────────────────────────────────────────────────

@router.post("/recommend", response_model=RecommendResponse)
async def get_recommendations(
    request: RecommendRequest,
    service: GraniteService = Depends(get_granite_service),  # 503 if creds missing
) -> RecommendResponse:
    """
    Get AI destination recommendations based on interests and budget.
    All cost estimates are labeled is_estimated=True.
    """
    logger.info(
        "recommend request: interests=%s budget=%.0f days=%d",
        request.interests, request.budget_usd, request.days,
    )

    raw_list = service.generate_recommendations(
        interests=request.interests,
        budget_usd=request.budget_usd,
        days=request.days,
    )

    items = []
    for item in raw_list:
        if not isinstance(item, dict):
            continue
        items.append(RecommendationItem(
            destination=_safe_str(item, "destination", "Unknown"),
            country=_safe_str(item, "country") or None,
            description=_safe_str(item, "description") or None,
            highlights=_safe_list(item, "highlights"),
            best_time_to_visit=_safe_str(item, "best_time_to_visit") or None,
            estimated_total_cost_usd=_safe_float(item, "estimated_total_cost_usd") or None,
            is_estimated=True,
            difficulty_level=_safe_str(item, "difficulty_level") or None,
        ))

    return RecommendResponse(
        recommendations=items,
        is_estimated=True,
        granite_model="ibm/granite-4-h-small",
    )


# ── /ai/budget ──────────────────────────────────────────────────────────────

@router.post("/budget", response_model=BudgetResponse)
async def estimate_budget(
    request: BudgetRequest,
    service: GraniteService = Depends(get_granite_service),  # 503 if creds missing
) -> BudgetResponse:
    """
    Estimate trip budget using IBM Granite.
    All returned figures are AI estimates (is_estimated=True).
    """
    logger.info(
        "budget request: destination=%s days=%d style=%s",
        request.destination, request.days, request.travel_style,
    )

    raw = service.estimate_budget(
        destination=request.destination,
        days=request.days,
        travel_style=request.travel_style,
    )

    breakdown_raw = raw.get("breakdown") or {}
    breakdown = BudgetBreakdown(
        accommodation_per_night_usd=_safe_float(breakdown_raw, "accommodation_per_night_usd"),
        food_per_day_usd=_safe_float(breakdown_raw, "food_per_day_usd"),
        transport_total_usd=_safe_float(breakdown_raw, "transport_total_usd"),
        activities_total_usd=_safe_float(breakdown_raw, "activities_total_usd"),
        miscellaneous_usd=_safe_float(breakdown_raw, "miscellaneous_usd"),
    ) if breakdown_raw else None

    return BudgetResponse(
        destination=_safe_str(raw, "destination", request.destination),
        days=int(raw.get("days", request.days)),
        travel_style=_safe_str(raw, "travel_style", request.travel_style),
        breakdown=breakdown,
        total_estimated_usd=_safe_float(raw, "total_estimated_usd"),
        is_estimated=True,
        notes=_safe_str(raw, "notes") or None,
        granite_model="ibm/granite-4-h-small",
        raw_ai_data=raw,
    )
