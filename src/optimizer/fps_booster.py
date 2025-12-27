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


def _lower_list(lst) -> list[str]:
    return [str(x).lower() for x in (lst or [])]


DEFAULT_EXCLUDED = _lower_list(settings.get("fps_booster", {}).get("excluded_processes", []))
NEVER_KILL = set(_lower_list(settings.get("fps_booster", {}).get("never_kill", [])))


def kill_background_processes(excluded_processes=None, dry_run: bool = False) -> dict:
    """
    If dry_run=True: does NOT kill anything, only reports what WOULD be killed.
    Always respects never_kill list.
    """
    excluded = set(_lower_list(excluded_processes)) if excluded_processes is not None else set(DEFAULT_EXCLUDED)
    unnecessary = set(_lower_list(UNNECESSARY_PROCESSES))

    killed_or_would = set()

    for proc in psutil.process_iter(["pid", "name"]):
        name = proc.info.get("name")
        if not name:
            continue

        n = name.lower()

        if n in NEVER_KILL:
            continue

        if n in unnecessary and n not in excluded:
            if dry_run:
                killed_or_would.add(name)
                continue

            try:
                proc.kill()
                killed_or_would.add(name)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

    items = sorted(killed_or_would)
    prefix = "[DRY-RUN] " if dry_run else ""
    log("fps_booster", f"{prefix}Killed processes: {items}")

    return {"killed_processes": items, "dry_run": dry_run}


def clear_ram() -> float:
    before = psutil.virtual_memory().used
    after = psutil.virtual_memory().used
    freed = round((before - after) / (1024 ** 2), 2)
    return max(freed, 0.0)


def boost_fps(excluded_processes=None) -> dict:
    dry_run = bool(settings.get("ux", {}).get("dry_run", False))
    result = kill_background_processes(excluded_processes, dry_run=dry_run)

    freed_ram = 0.0
    if not dry_run:
        freed_ram = clear_ram()

    prefix = "[DRY-RUN] " if dry_run else ""
    log("fps_booster", f"{prefix}Freed RAM: {freed_ram} MB")

    return {
        "killed_processes": result["killed_processes"],
        "freed_ram_mb": freed_ram,
        "dry_run": dry_run,
    }
