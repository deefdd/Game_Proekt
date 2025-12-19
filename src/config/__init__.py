import json
import sys
from pathlib import Path


def _candidate_paths():
    # 1) Папка, звідки запущено програму (для dist\config\settings.json)
    yield Path(sys.argv[0]).resolve().parent / "config" / "settings.json"
    yield Path.cwd() / "config" / "settings.json"

    # 2) Dev-режим (коли запускаєш python -m src.main)
    yield Path(__file__).resolve().parent / "settings.json"

    # 3) PyInstaller onefile temp dir (якщо будеш пакувати всередину)
    if hasattr(sys, "_MEIPASS"):
        yield Path(sys._MEIPASS) / "config" / "settings.json"


def load_settings():
    for p in _candidate_paths():
        if p.exists():
            with open(p, "r", encoding="utf-8") as f:
                return json.load(f)
    raise FileNotFoundError("settings.json not found in any expected location")


settings = load_settings()
