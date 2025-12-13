import sys
from pathlib import Path

# Add src to Python path
BASE_DIR = Path(__file__).resolve().parents[1] / "src"
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.optimizer.system_info import get_system_info



def run_tests():
    print("[test_system_info] Running...")
    info = get_system_info()

    assert isinstance(info, dict), "system_info should return a dict"

    required_keys = [
        "CPU",
        "CPU Cores",
        "RAM Total (GB)",
        "RAM Used (GB)",
        "RAM Free (GB)",
        "OS",
        "OS Version",
        "GPU Name",
        "GPU Load (%)",
        "GPU VRAM Total (GB)",
        "GPU VRAM Used (GB)",
    ]

    for key in required_keys:
        assert key in info, f"Missing key in system_info: {key}"

    print("[test_system_info] OK")
