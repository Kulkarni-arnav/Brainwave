import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

from backend.weather.open_meteo import (
    resolve_city,
    get_current_weather
)


def main():

    print("LIVE WEATHER EVALUATION")
    print("=" * 50)

    city = "Bhopal"

    try:
        location = resolve_city(city)

        if not location:
            print("FAIL: Could not resolve location.")
            return

        weather_data = get_current_weather(
            location["latitude"],
            location["longitude"]
        )

        weather = weather_data["current"]

        print(f"Location: {location['name']}")
        print(f"Time: {weather['time']}")
        print(
            f"Temperature: "
            f"{weather['temperature_2m']}°C"
        )
        print(
            f"Wind: "
            f"{weather['wind_speed_10m']} km/h"
        )
        print(
            f"Precipitation: "
            f"{weather['precipitation']} mm"
        )
        print(
            f"Precipitation probability: "
            f"{weather['precipitation_probability']}%"
        )

        severe = (
            weather["precipitation"] >= 10
            and
            weather["precipitation_probability"] >= 70
        )

        print("\nWhat checked:")
        print(
            "Whether the live API response contains "
            "the severe precipitation conditions used "
            "by the critical SOP."
        )

        if severe:
            print("Passed: PASS")
            print(
                "The live weather currently satisfies "
                "the severe precipitation thresholds."
            )
        else:
            print("Passed: NOT APPLICABLE")
            print(
                "The live weather does not currently "
                "meet the severe precipitation thresholds."
            )
            print(
                "This is expected because live weather "
                "changes. The deterministic severe-weather "
                "test provides reproducible coverage."
            )

    except Exception as error:

        print("Passed: FAIL")
        print(f"Live weather request failed: {error}")


if __name__ == "__main__":
    main()