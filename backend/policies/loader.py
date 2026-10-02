import json
from pathlib import Path


SOP_FILE = Path(__file__).parent / "sops.json"


def load_sops():
    with open(SOP_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data["sops"]