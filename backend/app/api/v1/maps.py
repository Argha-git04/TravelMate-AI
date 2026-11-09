"""
Maps endpoints — geocoding proxy using Nominatim / OpenStreetMap.
Free to use, no API key required.

Routes:
    GET /api/v1/maps/geocode?q={query}   — city name → lat/lon coordinates
"""
from fastapi import APIRouter

router = APIRouter(prefix="/maps", tags=["Maps"])


# TODO Phase 6: implement geocode endpoint
