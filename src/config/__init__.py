import json
import sys
from pathlib import Path


def _candidate_paths():
    # 1) EXE / dist mode: dist\config\settings.json
    yield Path(sys.argv[0]).resolve().parent / "config" / "settings.json"
    # 2) run from current folder: .\config\settings.json
    yield Path.cwd() / "config" / "settings.json"
    # 3) dev mode: src/config/settings.json
    yield Path(__file__).resolve().parent / "settings.json"
    # 4) PyInstaller onefile temp dir (якщо колись запаковуватимеш всередину)
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
    """Reload settings.json at runtime."""
    global settings
    settings = load_settings()
