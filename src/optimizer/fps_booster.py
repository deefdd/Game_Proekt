import psutil
from src.utils.logger import log



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
    "chrome_helper.exe"
]


DEFAULT_EXCLUDED_PROCESSES = [
    "discord.exe",
    "discorddevelopment.exe",
    "Chrome.exe",
]



def kill_background_processes(excluded_processes=None):

    if excluded_processes is None:
        excluded_processes = DEFAULT_EXCLUDED_PROCESSES

    excluded = {name.lower() for name in excluded_processes}
    unnecessary = {name.lower() for name in UNNECESSARY_PROCESSES}

    killed = []

    for proc in psutil.process_iter(['pid', 'name']):
        name = proc.info.get('name')
        if not name:
            continue

        n = name.lower()

        if n in unnecessary and n not in excluded:
            try:
                proc.kill()
                killed.append(name)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

    log("fps_booster", f"Killed processes: {killed}")
    return killed



def clear_ram():

    before = psutil.virtual_memory().used
    psutil.virtual_memory()
    after = psutil.virtual_memory().used

    freed = round((before - after) / (1024 ** 2), 2)
    return freed if freed > 0 else 0.0


def boost_fps(excluded_processes=None):
    killed = kill_background_processes(excluded_processes=excluded_processes)
    freed_ram = clear_ram()

    return {
        "killed_processes": killed,
        "freed_ram_mb": freed_ram
    }

