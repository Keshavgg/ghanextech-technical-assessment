"""
Tool: Live Weather Service
Provider: Open-Meteo REST API (Open-source, free, no API key required)
Author: Keshav Jindal
"""

import requests
from typing import Dict, Any

WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    71: "Slight snow fall",
    73: "Moderate snow fall",
    75: "Heavy snow fall",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail"
}

def get_current_weather(location: str) -> Dict[str, Any]:
    """
    Fetches real-time weather information for a given city or location.
    
    Parameters:
        location (str): Name of the city or locality (e.g., "New Delhi", "Tokyo", "London", "San Francisco").
        
    Returns:
        dict: Real-time weather data including temperature, wind speed, condition, and coordinates.
    """
    if not location or not location.strip():
        return {"error": "Location parameter cannot be empty."}

    loc_clean = location.strip()
    try:
        # Step 1: Geocode location to lat/lon via Open-Meteo Geocoding
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={requests.utils.quote(loc_clean)}&count=1&language=en&format=json"
        geo_res = requests.get(geo_url, timeout=6)
        if geo_res.status_code != 200:
            return {"error": f"Geocoding service returned HTTP {geo_res.status_code}."}

        geo_data = geo_res.json()
        results = geo_data.get("results")
        if not results:
            return {"error": f"Location '{loc_clean}' could not be resolved. Please verify the city name."}

        top_match = results[0]
        lat = top_match.get("latitude")
        lon = top_match.get("longitude")
        city_name = top_match.get("name")
        country = top_match.get("country", "")

        # Step 2: Fetch current weather
        weather_url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}&current_weather=true&hourly=relativehumidity_2m"
        )
        w_res = requests.get(weather_url, timeout=6)
        if w_res.status_code != 200:
            return {"error": f"Weather API returned HTTP {w_res.status_code}."}

        w_data = w_res.json()
        current = w_data.get("current_weather", {})
        temp_c = current.get("temperature")
        wind_kmh = current.get("windspeed")
        w_code = current.get("weathercode", -1)
        condition = WEATHER_CODES.get(w_code, "Unknown conditions")

        return {
            "success": True,
            "location": f"{city_name}, {country}".strip(", "),
            "temperature_celsius": temp_c,
            "temperature_fahrenheit": round((temp_c * 9/5) + 32, 1) if temp_c is not None else None,
            "condition": condition,
            "wind_speed_kmh": wind_kmh,
            "latitude": lat,
            "longitude": lon,
            "timestamp": current.get("time")
        }

    except requests.exceptions.Timeout:
        return {"error": "Weather lookup timed out. Please try again."}
    except Exception as e:
        return {"error": f"Failed to retrieve weather data: {str(e)}"}
