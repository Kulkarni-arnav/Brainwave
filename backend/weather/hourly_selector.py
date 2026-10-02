from datetime import datetime


def get_weather_for_time(hourly_weather, target_time):
    times = hourly_weather["hourly"]["time"]

    closest_index = None
    closest_difference = None

    for i, time_string in enumerate(times):
        forecast_time = datetime.fromisoformat(time_string)

        difference = abs(
            forecast_time - target_time
        )

        if closest_difference is None or difference < closest_difference:
            closest_difference = difference
            closest_index = i

    if closest_index is None:
        return None

    weather = {
        "time": times[closest_index],
        "temperature_2m": hourly_weather["hourly"]["temperature_2m"][closest_index],
        "wind_speed_10m": hourly_weather["hourly"]["wind_speed_10m"][closest_index],
        "precipitation": hourly_weather["hourly"]["precipitation"][closest_index],
        "precipitation_probability": hourly_weather["hourly"]["precipitation_probability"][closest_index],
        "uv_index": hourly_weather["hourly"]["uv_index"][closest_index]
    }

    return weather