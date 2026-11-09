"""
Weather endpoints — proxy to Open-Meteo (free, no API key required).
Returns live weather data clearly labeled is_live: true.

Routes:
    GET /api/v1/weather?city={city}   — current weather + forecast
"""
from fastapi import APIRouter

router = APIRouter(prefix="/weather", tags=["Weather"])


# TODO Phase 6: implement weather endpoint
