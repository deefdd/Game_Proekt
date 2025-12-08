import psutil
import platform
import GPUtil

def get_system_info():
    info = {
        "CPU": platform.processor(),
        "CPU Cores": psutil.cpu_count(logical=True),
        "RAM Total (GB)": round(psutil.virtual_memory().total / (1024 ** 3), 2),
        "RAM Used (GB)": round(psutil.virtual_memory().used / (1024 ** 3), 2),
        "RAM Free (GB)": round(psutil.virtual_memory().available / (1024 ** 3), 2),
        "OS": platform.system(),
        "OS Version": platform.version(),
    }

    gpus = GPUtil.getGPUs()
    if gpus:
        gpu = gpus[0]
        info["GPU Name"] = gpu.name
        info["GPU Load (%)"] = round(gpu.load * 100, 1)
        info["GPU VRAM Total (GB)"] = round(gpu.memoryTotal / 1024, 2)
        info["GPU VRAM Used (GB)"] = round(gpu.memoryUsed / 1024, 2)
    else:
        info["GPU"] = "Not detected"

    return info