"""
Shared / common Pydantic models used across multiple endpoints.

The is_estimated flag is the key data contract in TravelMate-AI:
- True  → price came from IBM Granite AI (never guaranteed)
- False → price came from a verified live source
"""
from pydantic import BaseModel


class PriceEstimate(BaseModel):
    """A monetary value that is always tagged with its reliability."""
    amount_usd: float
    is_estimated: bool = True       # Granite prices default to estimated
    currency: str = "USD"


class HealthResponse(BaseModel):
    status: str
    version: str
    environment: str
