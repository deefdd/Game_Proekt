import psutil

def get_system_info():
    cpu_percent = psutil.cpu_percent()
    ram = psutil.virtual_memory()
    
    return {
        "cpu_load": cpu_percent,
        "ram_used": ram.used // (1024 * 1024),
        "ram_total": ram.total // (1024 * 1024)
    }
