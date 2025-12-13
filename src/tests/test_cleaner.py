import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1] / "src"
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.optimizer.system_cleaner import clean_temp_files



def run_tests():
    print("[test_cleaner] Running...")

    result = clean_temp_files()

    assert isinstance(result, dict), "clean_temp_files should return a dict"

    for key in ["temp_removed", "windows_temp_removed", "chrome_cache_removed"]:
        assert key in result, f"Missing key: {key}"
        assert isinstance(result[key], int), f"{key} must be an int"

    print("[test_cleaner] OK")
