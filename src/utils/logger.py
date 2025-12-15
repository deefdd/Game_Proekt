import os
from datetime import datetime
from pathlib import Path
from src.config import settings

# Folder for logs
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

# Logging config from settings.json
logging_config = settings.get("logging", {})

AUTO_CLEANUP_DAYS = logging_config.get("auto_cleanup_days", 7)

MODULE_LOG_FLAGS = {
    "main": logging_config.get("save_main_log", True),
    "cleaner": logging_config.get("save_cleaner_log", True),
    "fps_booster": logging_config.get("save_fps_log", True),
    "system_info": logging_config.get("save_system_info_log", True),
    # other modules (advanced_cleaner, logger etc.) will default to True
}


def _is_logging_enabled(module: str) -> bool:
    """
    Returns True if logging is enabled for the given module.
    If module is not in MODULE_LOG_FLAGS, logging is enabled by default.
    """
    enabled = MODULE_LOG_FLAGS.get(module)
    if enabled is None:
        return True
    return enabled


def log(module: str, message: str) -> None:
    """
    Writes a standard log message to logs/<module>.log
    Respects logging flags from settings.json.
    """
    if not _is_logging_enabled(module):
        return

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_file = LOG_DIR / f"{module}.log"

    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")


def log_error(module: str, message: str) -> None:
    """
    Writes an ERROR log message to logs/<module>.log
    Also respects logging flags.
    """
    if not _is_logging_enabled(module):
        return

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_file = LOG_DIR / f"{module}.log"

    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] ERROR: {message}\n")


def cleanup_old_logs(days: int | None = None) -> None:
    """
    Deletes log files older than N days.
    If days is None, uses AUTO_CLEANUP_DAYS from settings.json.
    """
    if days is None:
        days = AUTO_CLEANUP_DAYS

    if days is None or days <= 0:
        return

    cutoff = datetime.now().timestamp() - days * 86400  # days → seconds

    for file in LOG_DIR.iterdir():
        if not file.is_file():
            continue

        try:
            if file.stat().st_mtime < cutoff:
                file.unlink()
        except Exception as e:
            # Always log logger errors into logger.log directly
            ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger_file = LOG_DIR / "logger.log"
            with open(logger_file, "a", encoding="utf-8") as f:
                f.write(f"[{ts}] ERROR: Could not delete log {file.name}: {e}\n")
