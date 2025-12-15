import json
from pathlib import Path

SETTINGS_PATH = Path(__file__).parent / "settings.json"

def load_settings():
    with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

settings = load_settings()
