import psutil
from src.utils.logger import log
from src.config import settings

UNNECESSARY_PROCESSES = [
    "OneDrive.exe",
    "EpicWebHelper.exe",
    "Telegram.exe",
    "firefox.exe",
    "msedge.exe",
    "slack.exe",
    "zoom.exe",
    "vlc.exe",
    "spotify.exe",
    "whatsapp.exe",
    "discord.exe",
    "opera.exe",
    "chrome.exe",
]

DEFAULT_EXCLUDED_PROCESSES = [
    p.lower() for p in settings.get("fps_booster", {}).get("excluded_processes", [])
]


def kill_background_processes(excluded_processes=None):
    if excluded_processes is None:
        excluded_processes = DEFAULT_EXCLUDED_PROCESSES

    excluded = {name.lower() for name in excluded_processes}
    unnecessary = {name.lower() for name in UNNECESSARY_PROCESSES}

    killed_set = set()

    for proc in psutil.process_iter(["pid", "name"]):
        name = proc.info.get("name")
        if not name:
            continue

        n = name.lower()
        if n in unnecessary and n not in excluded:
            try:
                proc.kill()
                killed_set.add(name)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

    killed_list = sorted(killed_set)
    log("fps_booster", f"Killed processes: {killed_list}")
    return killed_list


def clear_ram() -> float:
    before = psutil.virtual_memory().used
    after = psutil.virtual_memory().used
    freed = round((before - after) / (1024 ** 2), 2)
    return max(freed, 0.0)


def boost_fps(excluded_processes=None) -> dict:
    killed = kill_background_processes(excluded_processes)
    freed_ram = clear_ram()

    log("fps_booster", f"Freed RAM: {freed_ram} MB")

    return {"killed_processes": killed, "freed_ram_mb": freed_ram}
