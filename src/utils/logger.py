import os
from datetime import datetime
from pathlib import Path

# Folder for logs
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)


def log(module: str, message: str) -> None:
    """
    Writes a standard log message to logs/<module>.log
    """
    log_file = LOG_DIR / f"{module}.log"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")


def log_error(module: str, message: str) -> None:
    """
    Writes an ERROR log message to logs/<module>.log
    """
    log_file = LOG_DIR / f"{module}.log"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] ERROR: {message}\n")


def cleanup_old_logs(days: int = 7):
    """
    Deletes log files older than N days.
    """
    cutoff = datetime.now().timestamp() - days * 86400  # days → seconds

    for file in LOG_DIR.iterdir():
        if file.is_file():
            try:
                if file.stat().st_mtime < cutoff:
                    file.unlink()
            except Exception as e:
                log_error("logger", f"Could not delete log {file.name}: {e}")
