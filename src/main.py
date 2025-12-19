from src.utils.logger import log, log_error, cleanup_old_logs
from src.config import settings
from src.optimizer.system_info import get_system_info
from src.optimizer.fps_booster import boost_fps
from src.optimizer.system_cleaner import clean_temp_files
from src.optimizer.advanced_cleaner import advanced_cleaner


def main() -> None:
    # --- LOG: start + cleanup old logs ---
    log("main", "Program started")
    cleanup_old_logs()

    features = settings.get("features", {})

    # --- SYSTEM INFO ---
    if features.get("show_system_info", True):
        print("=== SYSTEM INFORMATION ===")
        system_info = get_system_info()
        for key, value in system_info.items():
            print(f"{key}: {value}")

    # --- FPS BOOSTER ---
    if features.get("boost_fps", True):
        print("\n=== FPS BOOSTER ===")
        booster_result = boost_fps()
        print(f"Killed processes: {booster_result['killed_processes']}")
        print(f"Freed RAM: {booster_result['freed_ram_mb']} MB")

    # --- BASIC SYSTEM CLEANER ---
    if features.get("clean_temp", True):
        print("\n=== SYSTEM CLEANER ===")
        clean_result = clean_temp_files()
        print("Removed TEMP files:", clean_result["temp_removed"])
        print("Removed Windows Temp:", clean_result["windows_temp_removed"])
        print("Removed Chrome Cache:", clean_result["chrome_cache_removed"])

    # --- ADVANCED CLEANER ---
    if features.get("advanced_clean", True):
        print("\n=== ADVANCED CLEANER ===")
        adv = advanced_cleaner()
        print(f"Removed Prefetch: {adv.get('prefetch_removed', 0)}")
        print(f"Removed Shader Cache: {adv.get('shader_cache_removed', 0)}")
        print(f"Removed Windows Update Cache: {adv.get('update_cache_removed', 0)}")


    # --- LOG: finish ---
    log("main", "Program finished successfully")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log_error("main", f"Unhandled error: {e}")
        raise
