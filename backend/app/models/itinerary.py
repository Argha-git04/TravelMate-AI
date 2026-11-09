"""
Pydantic models for AI endpoint requests and responses.

All cost fields carry is_estimated=True because they originate from IBM Granite.
The frontend reads this flag and renders "(estimated)" next to every price.

IMPORTANT: These models are used for both API validation and JSON serialization.
Fields with is_estimated=True must NEVER be presented as verified live prices.
"""
from __future__ import annotations

from typing import Optional, Any
from pydantic import BaseModel, Field, field_validator


# ════════════════════════════════════════════════════════════════
# Request Models
# ════════════════════════════════════════════════════════════════

class ItineraryRequest(BaseModel):
    destination: str = Field(..., min_length=2, max_length=200, description="Destination city and country")
    days: int = Field(..., ge=1, le=30, description="Trip duration in days")
    budget_usd: float = Field(..., gt=0, le=100_000, description="Total budget in USD")
    interests: list[str] = Field(..., min_length=1, max_length=10, description="List of traveler interests")
    start_date: Optional[str] = Field(None, description="ISO date string, e.g. 2026-06-01")
    travel_style: str = Field("mid-range", description="budget | mid-range | luxury")

    @field_validator("travel_style")
    @classmethod
    def validate_travel_style(cls, v: str) -> str:
        allowed = {"budget", "mid-range", "luxury"}
        if v not in allowed:
            raise ValueError(f"travel_style must be one of: {', '.join(allowed)}")
        return v

    @field_validator("interests")
    @classmethod
    def validate_interests(cls, v: list[str]) -> list[str]:
        return [i.strip() for i in v if i.strip()][:10]


class RecommendRequest(BaseModel):
    interests: list[str] = Field(..., min_length=1, max_length=10)
    budget_usd: float = Field(..., gt=0, le=100_000)
    days: int = Field(..., ge=1, le=30)

    @field_validator("interests")
    @classmethod
    def validate_interests(cls, v: list[str]) -> list[str]:
        return [i.strip() for i in v if i.strip()][:10]


class BudgetRequest(BaseModel):
    destination: str = Field(..., min_length=2, max_length=200)
    days: int = Field(..., ge=1, le=30)
    travel_style: str = Field("mid-range")

    @field_validator("travel_style")
    @classmethod
    def validate_travel_style(cls, v: str) -> str:
        allowed = {"budget", "mid-range", "luxury"}
        if v not in allowed:
            raise ValueError(f"travel_style must be one of: {', '.join(allowed)}")
        return v


# ════════════════════════════════════════════════════════════════
# Response Models — all prices carry is_estimated: true
# ════════════════════════════════════════════════════════════════

class ActivityResponse(BaseModel):
    time: Optional[str] = None
    name: str
    description: Optional[str] = None
    location_name: Optional[str] = None
    estimated_cost_usd: float = 0.0
    is_estimated: bool = True


class AccommodationResponse(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    estimated_cost_usd: float = 0.0
    is_estimated: bool = True


class TransportResponse(BaseModel):
    type: Optional[str] = None
    description: Optional[str] = None
    estimated_cost_usd: float = 0.0
    is_estimated: bool = True


class DayPlanResponse(BaseModel):
    day_number: int
    title: Optional[str] = None
    activities: list[ActivityResponse] = []
    accommodation: Optional[AccommodationResponse] = None
    transport: Optional[TransportResponse] = None
    day_estimated_total_usd: float = 0.0
    is_estimated: bool = True


class ItineraryResponse(BaseModel):
    destination: str
    duration_days: int
    total_estimated_cost_usd: float
    is_estimated: bool = True
    days: list[DayPlanResponse] = []
    travel_style: Optional[str] = None
    granite_model: str = "ibm/granite-4-h-small"

    # Raw AI data is also included so the frontend can access any extra fields
    raw_ai_data: Optional[dict] = None


class RecommendationItem(BaseModel):
    destination: str
    country: Optional[str] = None
    description: Optional[str] = None
    highlights: list[str] = []
    best_time_to_visit: Optional[str] = None
    estimated_total_cost_usd: Optional[float] = None
    is_estimated: bool = True
    difficulty_level: Optional[str] = None


class RecommendResponse(BaseModel):
    recommendations: list[RecommendationItem]
    is_estimated: bool = True
    granite_model: str = "ibm/granite-4-h-small"


class BudgetBreakdown(BaseModel):
    accommodation_per_night_usd: float = 0.0
    food_per_day_usd: float = 0.0
    transport_total_usd: float = 0.0
    activities_total_usd: float = 0.0
    miscellaneous_usd: float = 0.0


class BudgetResponse(BaseModel):
    destination: str
    days: int
    travel_style: str
    breakdown: Optional[BudgetBreakdown] = None
    total_estimated_usd: float
    is_estimated: bool = True
    notes: Optional[str] = None
    granite_model: str = "ibm/granite-4-h-small"
    raw_ai_data: Optional[dict] = None
