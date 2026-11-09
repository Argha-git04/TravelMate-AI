"""
Maps service — geocoding using Nominatim (OpenStreetMap).

Nominatim is completely free and requires no API key.
Converts city/place names to latitude/longitude coordinates.

API base: https://nominatim.openstreetmap.org/search
User-Agent header is required by Nominatim's usage policy.
"""

# TODO Phase 6: implement MapsService class
#   - geocode(query: str) -> dict
#     Returns: lat, lon, display_name
#   - reverse_geocode(lat: float, lon: float) -> dict
