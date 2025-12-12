


import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from optimizer.system_info import get_system_info
from optimizer.fps_booster import boost_fps
from optimizer.system_cleaner import clean_temp_files
from optimizer.advanced_cleaner import advanced_cleaner
from utils.logger import log, log_error, cleanup_old_logs

from utils.logger import log


def main():
    log("main", "Program started")
    cleanup_old_logs(7)
import time
start_time = time.time()

def main():
    # --- SYSTEM INFO ---
    print("=== SYSTEM INFORMATION ===")
    system_info = get_system_info()

    for key, value in system_info.items():
        print(f"{key}: {value}")

    # --- FPS BOOSTER ---
    print("\n=== FPS BOOSTER ===")

    excluded_processes = [
        "Discord.exe",   # keep Discord running
        "chrome.exe",    # keep Chrome running
    ]

    booster_result = boost_fps(excluded_processes=excluded_processes)

    print(f"Killed processes: {booster_result['killed_processes']}")
    print(f"Freed RAM: {booster_result['freed_ram_mb']} MB")

    # --- BASIC SYSTEM CLEANER ---
    print("\n=== SYSTEM CLEANER ===")
    clean_result = clean_temp_files()

    print("Removed TEMP files:", clean_result["temp_removed"])
    print("Removed Windows Temp:", clean_result["windows_temp_removed"])
    print("Removed Chrome Cache:", clean_result["chrome_cache_removed"])

    # --- ADVANCED CLEANER ---
    print("\n=== ADVANCED CLEANER ===")
    adv = advanced_cleaner()

    print(f"Removed Prefetch: {adv['prefetch_removed']}")
    print(f"Removed Shader Cache: {adv['shader_cache_removed']}")
    print(f"Removed Windows Update Cache: {adv['update_cache_removed']}")


if __name__ == "__main__":
    main()

duration = round(time.time() - start_time, 2)
log("main", f"Program finished successfully in {duration} seconds")


