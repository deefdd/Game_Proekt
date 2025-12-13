import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1] / "src"
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.optimizer.advanced_cleaner import advanced_cleaner



def run_tests():
    print("[test_advanced_cleaner] Running...")

    result = advanced_cleaner()

    assert isinstance(result, dict), "advanced_cleaner should return a dict"

    for key in ["prefetch_removed", "shader_cache_removed", "update_cache_removed"]:
        assert key in result, f"Missing key: {key}"
        assert isinstance(result[key], int), f"{key} must be an int"

    print("[test_advanced_cleaner] OK")
