"""
Open-Meteo weather service test.

Open-Meteo is free and requires no API key, so this test always runs.
It makes a real HTTP call to verify the integration works.

Run:
    cd backend
    conda run -n travelmate python -m pytest tests/test_weather.py -v
"""

# TODO Phase 6: add weather service tests
#   - test_geocode_returns_coordinates(): geocode "Paris" → lat/lon
#   - test_weather_returns_live_data(): get_weather("Paris") returns is_live: True
#   - test_weather_has_forecast(): response includes at least 3 forecast days
