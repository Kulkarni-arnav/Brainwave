from open_meteo import resolve_city, get_current_weather, get_hourly_weather


location = resolve_city("Bhopal")

print("LOCATION:")
print(location)

if location:
    weather = get_current_weather(
        location["latitude"],
        location["longitude"]
    )

    print("\nWEATHER:")
    print(weather)

    print("\nHOURLY WEATHER:")

    hourly_weather = get_hourly_weather(
        location["latitude"],
        location["longitude"]
    )

    for i in range(5):
        print(
            hourly_weather["hourly"]["time"][i],
            "| Temp:",
            hourly_weather["hourly"]["temperature_2m"][i],
            "| Wind:",
            hourly_weather["hourly"]["wind_speed_10m"][i],
            "| Rain:",
            hourly_weather["hourly"]["precipitation"][i],
            "| Rain probability:",
            hourly_weather["hourly"]["precipitation_probability"][i]
        )
else:
    print("Could not resolve location.")