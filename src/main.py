from src.utils.logger import log, log_error, cleanup_old_logs
from src.config import settings, reload_settings

from src.optimizer.system_info import get_system_info
from src.optimizer.fps_booster import boost_fps
from src.optimizer.system_cleaner import clean_temp_files
from src.optimizer.advanced_cleaner import advanced_cleaner


def _pause_if_needed():
    if settings.get("menu", {}).get("pause_after_action", True):
        input("\nPress Enter to continue...")


def _safe_mode_enabled() -> bool:
    return bool(settings.get("safe_mode", {}).get("enabled", False))


def run_all():
    print("=== SYSTEM INFORMATION ===")
    system_info = get_system_info()
    for k, v in system_info.items():
        print(f"{k}: {v}")

    print("\n=== FPS BOOSTER ===")
    if _safe_mode_enabled():
        print("⚠ Safe Mode enabled: skipping FPS Booster.")
    else:
        booster = boost_fps()
        print(f"Killed processes: {booster.get('killed_processes', [])}")
        print(f"Freed RAM: {booster.get('freed_ram_mb', 0.0)} MB")

    print("\n=== SYSTEM CLEANER ===")
    clean = clean_temp_files()
    print("Removed TEMP files:", clean.get("temp_removed", 0))
    print("Removed Windows Temp:", clean.get("windows_temp_removed", 0))
    print("Removed Chrome Cache:", clean.get("chrome_cache_removed", 0))

    print("\n=== ADVANCED CLEANER ===")
    if _safe_mode_enabled():
        print("⚠ Safe Mode enabled: skipping Advanced Cleaner.")
    else:
        adv = advanced_cleaner()
        print(f"Removed Prefetch: {adv.get('prefetch_removed', 0)}")
        print(f"Removed Shader Cache: {adv.get('shader_cache_removed', 0)}")
        print(f"Removed Windows Update Cache: {adv.get('update_cache_removed', 0)}")


def menu_loop():
    while True:
        safe = _safe_mode_enabled()

        print("\n=== GAME_PROEKT MENU ===")
        print("1) Show system info")
        print("2) Boost FPS" + ("  (SAFE MODE: OFF)" if not safe else "  (SAFE MODE: SKIPPED)"))
        print("3) Clean temp files")
        print("4) Advanced clean" + ("  (SAFE MODE: OFF)" if not safe else "  (SAFE MODE: SKIPPED)"))
        print("5) Run ALL")
        print("6) Reload settings.json")
        print(f"7) Toggle Safe Mode (currently: {safe})")
        print("0) Exit")

        choice = input("Select: ").strip()

        if choice == "0":
            return

        if choice == "1":
            info = get_system_info()
            print("\n=== SYSTEM INFORMATION ===")
            for k, v in info.items():
                print(f"{k}: {v}")
            _pause_if_needed()

        elif choice == "2":
            print("\n=== FPS BOOSTER ===")
            if _safe_mode_enabled():
                print("⚠ Safe Mode enabled: skipping FPS Booster.")
            else:
                res = boost_fps()
                print(f"Killed processes: {res.get('killed_processes', [])}")
                print(f"Freed RAM: {res.get('freed_ram_mb', 0.0)} MB")
            _pause_if_needed()

        elif choice == "3":
            print("\n=== SYSTEM CLEANER ===")
            res = clean_temp_files()
            print("Removed TEMP files:", res.get("temp_removed", 0))
            print("Removed Windows Temp:", res.get("windows_temp_removed", 0))
            print("Removed Chrome Cache:", res.get("chrome_cache_removed", 0))
            _pause_if_needed()

        elif choice == "4":
            print("\n=== ADVANCED CLEANER ===")
            if _safe_mode_enabled():
                print("⚠ Safe Mode enabled: skipping Advanced Cleaner.")
            else:
                adv = advanced_cleaner()
                print(f"Removed Prefetch: {adv.get('prefetch_removed', 0)}")
                print(f"Removed Shader Cache: {adv.get('shader_cache_removed', 0)}")
                print(f"Removed Windows Update Cache: {adv.get('update_cache_removed', 0)}")
            _pause_if_needed()

        elif choice == "5":
            run_all()
            _pause_if_needed()

        elif choice == "6":
            reload_settings()
            print("✅ Settings reloaded.")
            _pause_if_needed()

        elif choice == "7":
            # toggle safe mode in memory (до перезапуску/перезавантаження)
            if "safe_mode" not in settings:
                settings["safe_mode"] = {"enabled": False}
            settings["safe_mode"]["enabled"] = not bool(settings["safe_mode"].get("enabled", False))
            print(f"✅ Safe Mode is now: {settings['safe_mode']['enabled']}")
            _pause_if_needed()

        else:
            print("Unknown option.")


def main() -> None:
    log("main", "Program started")
    cleanup_old_logs()

    use_menu = settings.get("menu", {}).get("enabled", True)
    if use_menu:
        menu_loop()
    else:
        run_all()

    log("main", "Program finished successfully")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log_error("main", f"Unhandled error: {e}")
        raise
