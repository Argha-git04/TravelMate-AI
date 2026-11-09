"""
Itinerary endpoints — CRUD operations backed by IBM Cloudant Lite.

Routes:
    GET    /api/v1/itineraries        — list all saved itineraries
    GET    /api/v1/itineraries/{id}   — get a single itinerary
    POST   /api/v1/itineraries        — save a new itinerary
    DELETE /api/v1/itineraries/{id}   — delete an itinerary
"""
from fastapi import APIRouter

router = APIRouter(prefix="/itineraries", tags=["Itineraries"])


# TODO Phase 5: implement list endpoint
# TODO Phase 5: implement get-by-id endpoint
# TODO Phase 5: implement create endpoint
# TODO Phase 5: implement delete endpoint
