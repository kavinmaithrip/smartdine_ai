import os
import time
import requests
from dotenv import load_dotenv
load_dotenv()


# ---------------- CONFIG ---------------- #

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# Cache: city -> (timestamp, data)
_WEATHER_CACHE = {}

# Cache TTL (seconds)
CACHE_TTL = 600  # 10 minutes


# ---------------- HELPERS ---------------- #

def _classify_weather(temp_c, condition):
    """
    Convert raw weather into food-relevant categories.
    """
    if temp_c >= 30:
        return "hot"
    if temp_c <= 18:
        return "cold"
    if "rain" in condition.lower():
        return "rainy"
    if "cloud" in condition.lower():
        return "cloudy"
    return "pleasant"


# ---------------- MAIN API ---------------- #

def get_weather(city: str):
    """
    Returns weather context for a city.
    Cached to avoid repeated API calls.
    """

    if not API_KEY:
        # Fail-safe: no API key
        return {
            "city": city,
            "temp_c": None,
            "condition": "unknown",
            "category": "unknown"
        }

    city_key = city.lower().strip()
    now = time.time()

    # -------- CACHE HIT -------- #
    if city_key in _WEATHER_CACHE:
        ts, data = _WEATHER_CACHE[city_key]
        if now - ts < CACHE_TTL:
            return data

    # -------- API CALL -------- #
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    try:
        res = requests.get(BASE_URL, params=params, timeout=5)
        res.raise_for_status()
        payload = res.json()

        temp_c = round(payload["main"]["temp"])
        raw_condition = payload["weather"][0]["main"]

        weather_data = {
            "city": city,
            "temp_c": temp_c,
            "condition": raw_condition,
            "category": _classify_weather(temp_c, raw_condition)
        }

        # Save to cache
        _WEATHER_CACHE[city_key] = (now, weather_data)
        return weather_data

    except Exception:
        # Fail-safe fallback
        return {
            "city": city,
            "temp_c": None,
            "condition": "unknown",
            "category": "unknown"
        }
