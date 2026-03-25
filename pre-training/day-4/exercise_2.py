import json
import sys

import requests  # type: ignore[import-untyped]
from typing import Any, Optional


WMO_WEATHER_CODES = {
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
    71: "Slight snow",
    73: "Moderate snow",
    75: "Heavy snow",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    95: "Thunderstorm",
}


def get_json(url: str, params: Optional[dict[str, Any]] = None) -> tuple[Optional[requests.Response], Optional[Any]]:
    try:
        r = requests.get(url, params=params, timeout=15)
        return r, r.json()
    except requests.exceptions.RequestException:
        return None, None
    except ValueError:
        return r, None


def c_to_f(c: float) -> float:
    return (c * 9 / 5) + 32


def main() -> int:
    city = "Karachi"
    if len(sys.argv) >= 2 and sys.argv[1].strip():
        city = sys.argv[1].strip()

    geo_url = "https://geocoding-api.open-meteo.com/v1/search"
    r, geo = get_json(geo_url, params={"name": city, "count": 1, "language": "en", "format": "json"})
    if r is None:
        print("Network error: could not reach Open-Meteo geocoding.", file=sys.stderr)
        return 1

    if r.status_code != 200 or not isinstance(geo, dict):
        print(f"Unexpected geocoding response: {r.status_code}", file=sys.stderr)
        return 1

    print("RAW JSON (geocoding):")
    print(json.dumps(geo, indent=2))
    print()

    results = geo.get("results") or []
    if not results:
        print(f"City not found: {city}", file=sys.stderr)
        return 1

    place = results[0]
    name = place.get("name")
    country = place.get("country")
    latitude = place.get("latitude")
    longitude = place.get("longitude")
    if latitude is None or longitude is None:
        print("Unexpected geocoding result (missing coordinates).", file=sys.stderr)
        return 1

    weather_url = "https://api.open-meteo.com/v1/forecast"
    r2, weather = get_json(
        weather_url,
        params={
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,wind_speed_10m,weather_code",
            "temperature_unit": "celsius",
            "wind_speed_unit": "kmh",
        },
    )
    if r2 is None:
        print("Network error: could not reach Open-Meteo weather.", file=sys.stderr)
        return 1

    if r2.status_code != 200 or not isinstance(weather, dict):
        print(f"Unexpected weather response: {r2.status_code}", file=sys.stderr)
        return 1

    print("RAW JSON (weather):")
    print(json.dumps(weather, indent=2))
    print()

    current = weather.get("current") or {}
    temp_c = current.get("temperature_2m")
    wind_kmh = current.get("wind_speed_10m")
    code = current.get("weather_code")
    if temp_c is None or wind_kmh is None or code is None:
        print("Unexpected weather response (missing current fields).", file=sys.stderr)
        return 1
    description = WMO_WEATHER_CODES.get(code, "Unknown")

    print("WEATHER")
    print("city:", f"{name}, {country}")
    print("temperature:", f"{temp_c}°C / {c_to_f(temp_c):.1f}°F")
    print("wind speed:", f"{wind_kmh} km/h")
    print("description:", description)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

