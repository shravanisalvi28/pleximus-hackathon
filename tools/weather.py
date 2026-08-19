"""
Weather tool — fetches current weather using Open-Meteo (no API key required).
Geocoding is done via the Open-Meteo Geocoding API (also free, no key needed).
"""

import requests


GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

# WMO weather interpretation codes
WMO_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Foggy",
    48: "Icy fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    71: "Slight snow",
    73: "Moderate snow",
    75: "Heavy snow",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    95: "Thunderstorm",
    96: "Thunderstorm with hail",
    99: "Thunderstorm with heavy hail",
}


def _get_coordinates(city: str):
    """
    Convert a city name to (latitude, longitude, display_name) using Open-Meteo Geocoding API.
    Returns None if not found.
    """
    try:
        response = requests.get(
            GEOCODING_URL,
            params={"name": city, "count": 1, "language": "en", "format": "json"},
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.ConnectionError:
        return None, None, None, "Network error: Could not connect to geocoding service."
    except requests.exceptions.Timeout:
        return None, None, None, "Request timed out while looking up city coordinates."
    except requests.exceptions.RequestException as e:
        return None, None, None, f"Geocoding request failed: {e}"

    results = data.get("results")
    if not results:
        return None, None, None, f"City not found: '{city}'. Please check the spelling."

    location = results[0]
    lat = location.get("latitude")
    lon = location.get("longitude")
    name = location.get("name", city)
    country = location.get("country", "")
    display = f"{name}, {country}" if country else name
    return lat, lon, display, None


def get_weather(city: str) -> str:
    """
    Fetch current weather for a city and return a formatted summary.

    Args:
        city: Name of the city (e.g., "Mumbai", "London", "Ratnagiri").

    Returns:
        A human-readable weather summary string.
    """
    city = city.strip()

    lat, lon, display_name, error = _get_coordinates(city)
    if error:
        return error

    try:
        response = requests.get(
            WEATHER_URL,
            params={
                "latitude": lat,
                "longitude": lon,
                "current_weather": True,
                "hourly": "relative_humidity_2m",
                "forecast_days": 1,
                "timezone": "auto",
            },
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.ConnectionError:
        return "Network error: Could not connect to weather service."
    except requests.exceptions.Timeout:
        return "Request timed out while fetching weather data."
    except requests.exceptions.RequestException as e:
        return f"Weather request failed: {e}"

    current = data.get("current_weather")
    if not current:
        return f"No weather data available for {display_name}."

    temp = current.get("temperature", "N/A")
    wind = current.get("windspeed", "N/A")
    wmo_code = current.get("weathercode", -1)
    condition = WMO_CODES.get(wmo_code, "Unknown condition")

    return (
        f"Current weather in {display_name}:\n"
        f"  Temperature : {temp}°C\n"
        f"  Wind speed  : {wind} km/h\n"
        f"  Condition   : {condition}"
    )
