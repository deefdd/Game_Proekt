import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1] / "src"
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.optimizer.fps_booster import boost_fps



def run_tests():
    print("[test_fps_booster] Running...")

    result = boost_fps(excluded_processes=["Discord.exe", "chrome.exe"])

    assert isinstance(result, dict), "boost_fps should return a dict"
    assert "killed_processes" in result, "Missing key: killed_processes"
    assert "freed_ram_mb" in result, "Missing key: freed_ram_mb"

    assert isinstance(result["killed_processes"], list), "killed_processes must be a list"
    assert isinstance(result["freed_ram_mb"], (int, float)), "freed_ram_mb must be a number"

    print("[test_fps_booster] OK")
