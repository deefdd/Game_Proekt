from optimizer.system_cleaner import clean_temp_files
import sys
from pathlib import Path

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from optimizer.system_info import get_system_info
from optimizer.fps_booster import boost_fps


def main():
    print("=== SYSTEM INFORMATION ===")
    system_info = get_system_info()

    for key, value in system_info.items():
        print(f"{key}: {value}")

    print("\n=== FPS BOOSTER ===")

    
    excluded_processes = [
        "Discord.exe",   
        "chrome.exe",  
    ]

    booster_result = boost_fps(excluded_processes=excluded_processes)

    print(f"Killed processes: {booster_result['killed_processes']}")
    print(f"Freed RAM: {booster_result['freed_ram_mb']} MB")


if __name__ == "__main__":
    main()

print("\n=== SYSTEM CLEANER ===")
clean_result = clean_temp_files()

print("Removed TEMP files:", clean_result["temp_removed"])
print("Removed Windows Temp:", clean_result["windows_temp_removed"])
print("Removed Chrome Cache:", clean_result["chrome_cache_removed"])
