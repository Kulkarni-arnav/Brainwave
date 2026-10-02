from loader import load_sops
from matcher import match_sops, select_sop


sops = load_sops()


weather = {
    "temperature_2m": 30,
    "wind_speed_10m": 45,
    "precipitation": 12,
    "precipitation_probability": 80,
    "uv_index": 5
}


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


selected = select_sop(matched)

print("\nSELECTED SOP:")

if selected:
    print(selected["id"], "-", selected["name"])
else:
    print("No SOP matched")