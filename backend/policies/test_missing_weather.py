from loader import load_sops
from matcher import match_sops, MissingWeatherDataError


sops = load_sops()


weather = {
    "temperature_2m": 30,
    "wind_speed_10m": 20
}


try:
    matched = match_sops(
        sops,
        "cycling",
        weather
    )

    print("MATCHED SOPs:")

    for sop in matched:
        print(
            sop["id"],
            "-",
            sop["name"],
            "-",
            sop["severity"]
        )

except MissingWeatherDataError as error:
    print("WEATHER DATA ERROR:")
    print(error)