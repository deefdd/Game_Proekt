import os
import shutil
from pathlib import Path
from src.utils.logger import log
from src.config import settings   




# Paths to clean
TEMP_PATH = Path(os.getenv("TEMP"))
WINDOWS_TEMP_PATH = Path("C:/Windows/Temp")

CHROME_CACHE_PATH = Path(
    Path.home() / "AppData/Local/Google/Chrome/User Data/Default/Cache"
)


def delete_in_directory(path: Path) -> int:
    """
    Deletes files and folders inside a directory.
    Returns the number of removed items.
    If access is denied, returns 0 and does not crash the program.
    """
    if not path.exists() or not path.is_dir():
        return 0

    removed_count = 0

    try:
        items = list(path.iterdir())
    except PermissionError:
        # No access to this directory – skip it
        return 0

    for item in items:
        try:
            if item.is_file():
                item.unlink()
                removed_count += 1
            elif item.is_dir():
                shutil.rmtree(item, ignore_errors=True)
                removed_count += 1
        except PermissionError:
            # Skip files/folders we can't delete
            continue
        except Exception:
            # Ignore other unexpected errors
            continue

    return removed_count


def clean_temp_files() -> dict:
    removed_temp = 0
    removed_windows_temp = 0
    removed_chrome = 0

    if settings["cleaner"]["remove_temp"]:
        removed_temp = delete_in_directory(TEMP_PATH)

    if settings["cleaner"]["remove_windows_temp"]:
        removed_windows_temp = delete_in_directory(WINDOWS_TEMP_PATH)

    if settings["cleaner"]["remove_chrome_cache"]:
        removed_chrome = delete_in_directory(CHROME_CACHE_PATH)

    log("cleaner", f"Removed TEMP: {removed_temp}")
    log("cleaner", f"Removed Windows Temp: {removed_windows_temp}")
    log("cleaner", f"Removed Chrome Cache: {removed_chrome}")

    return {
        "temp_removed": removed_temp,
        "windows_temp_removed": removed_windows_temp,
        "chrome_cache_removed": removed_chrome
    }
