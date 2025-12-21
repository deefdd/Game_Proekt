import os
import shutil
from pathlib import Path
from src.utils.logger import log
from src.config import settings

TEMP_PATH = Path(os.getenv("TEMP"))
WINDOWS_TEMP_PATH = Path("C:/Windows/Temp")
CHROME_CACHE_PATH = Path(Path.home() / "AppData/Local/Google/Chrome/User Data/Default/Cache")


def delete_in_directory(path: Path, dry_run: bool = False) -> int:
    if not path.exists() or not path.is_dir():
        return 0

    try:
        items = list(path.iterdir())
    except PermissionError:
        return 0

    if dry_run:
        return len(items)

    removed = 0
    for item in items:
        try:
            if item.is_file():
                item.unlink()
                removed += 1
            elif item.is_dir():
                shutil.rmtree(item, ignore_errors=True)
                removed += 1
        except Exception:
            continue
    return removed


def clean_temp_files() -> dict:
    dry_run = settings.get("ux", {}).get("dry_run", False)

    removed_temp = removed_windows_temp = removed_chrome = 0

    if settings["cleaner"]["remove_temp"]:
        removed_temp = delete_in_directory(TEMP_PATH, dry_run=dry_run)

    if settings["cleaner"]["remove_windows_temp"]:
        removed_windows_temp = delete_in_directory(WINDOWS_TEMP_PATH, dry_run=dry_run)

    if settings["cleaner"]["remove_chrome_cache"]:
        removed_chrome = delete_in_directory(CHROME_CACHE_PATH, dry_run=dry_run)

    prefix = "[DRY-RUN] " if dry_run else ""
    log("cleaner", f"{prefix}Removed TEMP: {removed_temp}")
    log("cleaner", f"{prefix}Removed Windows Temp: {removed_windows_temp}")
    log("cleaner", f"{prefix}Removed Chrome Cache: {removed_chrome}")

    return {
        "temp_removed": removed_temp,
        "windows_temp_removed": removed_windows_temp,
        "chrome_cache_removed": removed_chrome,
        "dry_run": dry_run
    }
