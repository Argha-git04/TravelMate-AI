"""
Weather service — fetches live weather data from Open-Meteo.

Open-Meteo is completely free and requires no API key.
All data returned is live and labeled is_live: true.

API base: https://api.open-meteo.com/v1/forecast
Geocoding: https://geocoding-api.open-meteo.com/v1/search
"""

# TODO Phase 6: implement WeatherService class
#   - get_weather(city: str) -> dict
#     Returns: current_temp_c, condition, forecast (7 days), is_live: True
#   - _geocode_city(city: str) -> tuple[float, float]  (lat, lon)
