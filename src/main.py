from src.utils.logger import log, log_error, cleanup_old_logs
from src.config import settings, reload_settings

from src.optimizer.system_info import get_system_info
from src.optimizer.fps_booster import boost_fps
from src.optimizer.system_cleaner import clean_temp_files
from src.optimizer.advanced_cleaner import advanced_cleaner


def _pause_if_needed() -> None:
    if settings.get("menu", {}).get("pause_after_action", True):
        input("\nPress Enter to continue...")


def _safe_mode_enabled() -> bool:
    return bool(settings.get("safe_mode", {}).get("enabled", False))


def _dry_run_enabled() -> bool:
    return bool(settings.get("ux", {}).get("dry_run", False))


def _confirm(msg: str) -> bool:
    # якщо confirm вимкнений — завжди дозволяємо
    if not settings.get("ux", {}).get("confirm_dangerous_actions", True):
        return True
    ans = input(f"{msg} (y/n): ").strip().lower()
    return ans == "y"


def _print_system_info() -> None:
    print("\n=== SYSTEM INFORMATION ===")
    info = get_system_info()
    for k, v in info.items():
        print(f"{k}: {v}")


def _run_fps_booster() -> None:
    print("\n=== FPS BOOSTER ===")
    if _safe_mode_enabled():
        print("⚠ Safe Mode enabled: skipping FPS Booster.")
        return

    if not _confirm("This may close background apps. Continue?"):
        print("Cancelled.")
        return

    res = boost_fps()
    print(f"Killed processes: {res.get('killed_processes', [])}")
    print(f"Freed RAM: {res.get('freed_ram_mb', 0.0)} MB")


def _run_cleaner() -> None:
    print("\n=== SYSTEM CLEANER ===")
    dry = _dry_run_enabled()
    if dry:
        print("🟡 DRY-RUN: preview only (no files will be deleted).")

    res = clean_temp_files()
    print("Removed TEMP files:", res.get("temp_removed", 0))
    print("Removed Windows Temp:", res.get("windows_temp_removed", 0))
    print("Removed Chrome Cache:", res.get("chrome_cache_removed", 0))


def _run_advanced_cleaner() -> None:
    print("\n=== ADVANCED CLEANER ===")
    if _safe_mode_enabled():
        print("⚠ Safe Mode enabled: skipping Advanced Cleaner.")
        return

    if not _confirm("This will delete cache files. Continue?"):
        print("Cancelled.")
        return

    dry = _dry_run_enabled()
    if dry:
        print("🟡 DRY-RUN: preview only (no files will be deleted).")

    adv = advanced_cleaner()
    print(f"Removed Prefetch: {adv.get('prefetch_removed', 0)}")
    print(f"Removed Shader Cache: {adv.get('shader_cache_removed', 0)}")
    print(f"Removed Windows Update Cache: {adv.get('update_cache_removed', 0)}")


def run_all() -> None:
    _print_system_info()
    _run_fps_booster()
    _run_cleaner()
    _run_advanced_cleaner()


def menu_loop() -> None:
    while True:
        safe = _safe_mode_enabled()
        dry = _dry_run_enabled()

        print("\n=== GAME_PROEKT MENU ===")
        print("1) Show system info")
        print(f"2) Boost FPS {'(SKIPPED: SAFE MODE)' if safe else ''}")
        print(f"3) Clean temp files {'(DRY-RUN)' if dry else ''}")
        print(f"4) Advanced clean {'(SKIPPED: SAFE MODE)' if safe else ''} {'(DRY-RUN)' if dry else ''}")
        print("5) Run ALL")
        print("6) Reload settings.json")
        print(f"7) Toggle Safe Mode (currently: {safe})")
        print(f"8) Toggle Dry-Run (currently: {dry})")
        print("0) Exit")

        choice = input("Select: ").strip()

        if choice == "0":
            return

        if choice == "1":
            _print_system_info()
            _pause_if_needed()

        elif choice == "2":
            _run_fps_booster()
            _pause_if_needed()

        elif choice == "3":
            _run_cleaner()
            _pause_if_needed()

        elif choice == "4":
            _run_advanced_cleaner()
            _pause_if_needed()

        elif choice == "5":
            run_all()
            _pause_if_needed()

        elif choice == "6":
            reload_settings()
            print("✅ Settings reloaded.")
            _pause_if_needed()

        elif choice == "7":
            if "safe_mode" not in settings:
                settings["safe_mode"] = {"enabled": False}
            settings["safe_mode"]["enabled"] = not bool(settings["safe_mode"].get("enabled", False))
            print(f"✅ Safe Mode is now: {settings['safe_mode']['enabled']}")
            _pause_if_needed()

        elif choice == "8":
            if "ux" not in settings:
                settings["ux"] = {}
            settings["ux"]["dry_run"] = not bool(settings["ux"].get("dry_run", False))
            print(f"✅ Dry-Run is now: {settings['ux']['dry_run']}")
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
