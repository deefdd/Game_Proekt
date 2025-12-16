import psutil
from src.utils.logger import log
from src.config import settings

# Processes that are usually not needed while gaming
UNNECESSARY_PROCESSES = [
    "OneDrive.exe",
    "EpicWebHelper.exe",
    "Telegram.exe",
    "firefox.exe",
    "firefox_helper.exe",
    "msedge.exe",
    "msedge_proxy.exe",
    "powerpnt.exe",
    "slack.exe",
    "zoom.exe",
    "vlc.exe",
    "spotify.exe",
    "whatsapp.exe",
    "discord.exe",
    "discordptb.exe",
    "discordcanary.exe",
    "discorddevelopment.exe",
    "minecraftlauncher.exe",
    "minecraftpe.exe",
    "minecraftlauncherapp.exe",
    "opera.exe",
    "opera_gpu.exe",
    "chrome.exe",
    "chrome_helper.exe",
]

# Use excluded processes from settings.json
DEFAULT_EXCLUDED_PROCESSES = [
    p.lower() for p in settings["fps_booster"]["excluded_processes"]
]


def kill_background_processes(excluded_processes=None):
    """
    Kills unnecessary background processes
    except ones listed in excluded_processes.
    Returns a list of killed process names.
    """
    if excluded_processes is None:
        excluded_processes = DEFAULT_EXCLUDED_PROCESSES

    excluded = {name.lower() for name in excluded_processes}
    unnecessary = {name.lower() for name in UNNECESSARY_PROCESSES}

    killed = []

    for proc in psutil.process_iter(["pid", "name"]):
        name = proc.info.get("name")
        if not name:
            continue

        n = name.lower()

        if n in unnecessary and n not in excluded:
            try:
                proc.kill()
                killed.append(name)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

    log("fps_booster", f"Killed processes: {killed}")
    return killed


def clear_ram() -> float:
    """
    Dummy RAM cleanup placeholder.
    Right now it only measures RAM usage difference,
    but does not force any real RAM cleanup.
    """
    before = psutil.virtual_memory().used
    after = psutil.virtual_memory().used
    freed = round((before - after) / (1024 ** 2), 2)
    return max(freed, 0.0)


def boost_fps(excluded_processes=None) -> dict:
    """
    Main FPS booster function.
    Kills background processes and tries to free some RAM.
    """
    killed = kill_background_processes(excluded_processes)
    freed_ram = clear_ram()

    log("fps_booster", f"Freed RAM: {freed_ram} MB")

    return {
        "killed_processes": killed,
        "freed_ram_mb": freed_ram,
    }
