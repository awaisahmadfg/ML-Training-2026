"""
Exercise 2 - Weather CLI

Flow:
1) City name -> Open-Meteo Geocoding API
2) Coordinates -> Open-Meteo Forecast API (current weather)
"""

import json

import requests


def celsius_to_fahrenheit(temp_c: float) -> float:
    # C to F conversion formula.
    return (temp_c * 9 / 5) + 32


def weather_code_to_description(code: int) -> str:
    # Open-Meteo weather code mapping (common values).
    mapping = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        56: "Light freezing drizzle",
        57: "Dense freezing drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        66: "Light freezing rain",
        67: "Heavy freezing rain",
        71: "Slight snow fall",
        73: "Moderate snow fall",
        75: "Heavy snow fall",
        77: "Snow grains",
        80: "Slight rain showers",
        81: "Moderate rain showers",
        82: "Violent rain showers",
        85: "Slight snow showers",
        86: "Heavy snow showers",
        95: "Thunderstorm",
        96: "Thunderstorm with slight hail",
        99: "Thunderstorm with heavy hail",
    }
    return mapping.get(code, "Unknown weather condition")


def fetch_city_coordinates(city: str) -> dict:
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {
        "name": city,
        "count": 1,
        "language": "en",
        "format": "json",
    }

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()

    results = data.get("results", [])
    if not results:
        raise ValueError(f"City '{city}' not found in geocoding results.")
    return results[0]


def fetch_current_weather(latitude: float, longitude: float) -> dict:
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": ["temperature_2m", "wind_speed_10m", "weather_code"],
    }

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()

    current = data.get("current")
    if not current:
        raise ValueError("Current weather data not available from API.")
    return current


def print_raw_json_preview(location: dict, current: dict) -> None:
    # first geocoding response shape preview.
    print("\n=== RAW JSON (geocoding result) ===")
    print(json.dumps(location, indent=2))

    # then weather response shape preview.
    print("\n=== RAW JSON (current weather) ===")
    print(json.dumps(current, indent=2))


def main() -> None:
    print("Weather CLI (Open-Meteo)")
    city = input("Enter city name: ").strip()

    if not city:
        print("City name empty nahi ho sakta.")
        return

    try:
        # first API call: city -> lat/lon
        location = fetch_city_coordinates(city)
        latitude = float(location["latitude"])
        longitude = float(location["longitude"])

        # second API call: lat/lon -> current weather
        current = fetch_current_weather(latitude, longitude)
        print_raw_json_preview(location, current)

        temp_c = float(current["temperature_2m"])
        temp_f = celsius_to_fahrenheit(temp_c)
        wind_speed = float(current["wind_speed_10m"])
        weather_code = int(current["weather_code"])

        display_city = location.get("name", city)
        country = location.get("country", "Unknown country")
        description = weather_code_to_description(weather_code)

        print("\n=== Current Weather ===")
        print(f"City: {display_city}, {country}")
        print(f"Temperature: {temp_c:.1f} C / {temp_f:.1f} F")
        print(f"Wind Speed: {wind_speed:.1f} km/h")
        print(f"Description: {description} (code {weather_code})")
    except ValueError as err:
        print("Data error:", err)
    except requests.exceptions.Timeout:
        print("Request timeout. Internet/API slow ho sakti hai, dobara try karo.")
    except requests.exceptions.HTTPError as err:
        print("HTTP error from API:", err)
    except requests.exceptions.RequestException as err:
        print("Network/request issue:", err)


if __name__ == "__main__":
    main()
