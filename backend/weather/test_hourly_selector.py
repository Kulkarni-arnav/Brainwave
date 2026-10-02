from open_meteo import resolve_city, get_hourly_weather
from time_resolver import resolve_time
from hourly_selector import get_weather_for_time


location = resolve_city("Bhopal")

if location:
    hourly_weather = get_hourly_weather(
        location["latitude"],
        location["longitude"]
    )

    target_time = resolve_time("this evening")

    weather = get_weather_for_time(
        hourly_weather,
        target_time
    )

    print("TARGET TIME:")
    print(target_time)

    print("\nSELECTED WEATHER:")
    print(weather)
else:
    print("Could not resolve location.")