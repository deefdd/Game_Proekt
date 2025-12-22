import json
from pathlib import Path

PROFILES_DIR = Path("profiles")

def list_profiles() -> list[str]:
    if not PROFILES_DIR.exists():
        return []
    return sorted([p.stem for p in PROFILES_DIR.glob("*.json")])

def load_profile(name: str) -> dict:
    path = PROFILES_DIR / f"{name}.json"
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def deep_update(base: dict, patch: dict) -> dict:
    for k, v in patch.items():
        if isinstance(v, dict) and isinstance(base.get(k), dict):
            deep_update(base[k], v)
        else:
            base[k] = v
    return base
