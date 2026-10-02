# to make HTTP requests to the Open-Meteo API.
import requests 


GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"


def resolve_city(city):
    params = {
        "name": city,
        # for first geocoding result, we can set the count to 1
        "count": 1, 
        "language": "en",
        "format": "json"
    }

    # using requests to make a GET request to the Open-Meteo geocoding API with the specified parameters. 
    response = requests.get(GEOCODING_URL, params=params, timeout=10)
    response.raise_for_status()

    data = response.json()

    if "results" not in data or len(data["results"]) == 0:
        return None

    location = data["results"][0]

    return {
        "name": location["name"],
        "latitude": location["latitude"],
        "longitude": location["longitude"],
        "country": location.get("country")
    }


def get_current_weather(latitude, longitude):
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": (
            "temperature_2m,"
            "wind_speed_10m,"
            "precipitation,"
            "precipitation_probability,"
            "uv_index"
        )
    }

    response = requests.get(WEATHER_URL, params=params, timeout=10)
    response.raise_for_status()

    data = response.json()

    return data


def get_hourly_weather(latitude, longitude):
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": (
            "temperature_2m,"
            "wind_speed_10m,"
            "precipitation,"
            "precipitation_probability,"
            "uv_index"
        ),
        "forecast_days": 2,
        "timezone": "auto"
    }

    response = requests.get(
        WEATHER_URL,
        params=params,
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    return data
