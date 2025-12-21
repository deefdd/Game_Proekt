import json
import sys
from pathlib import Path


def _candidate_paths():
    yield Path(sys.argv[0]).resolve().parent / "config" / "settings.json"
    yield Path.cwd() / "config" / "settings.json"
    yield Path(__file__).resolve().parent / "settings.json"
    if hasattr(sys, "_MEIPASS"):
        yield Path(sys._MEIPASS) / "config" / "settings.json"


def load_settings() -> dict:
    for p in _candidate_paths():
        if p.exists():
            with open(p, "r", encoding="utf-8") as f:
                return json.load(f)
    raise FileNotFoundError("settings.json not found in any expected location")


settings: dict = load_settings()


def reload_settings() -> None:
    global settings
    settings.clear()
    settings.update(load_settings())
