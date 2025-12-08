from optimizer.system_info import get_system_info

info = get_system_info()
print("Стан системи:")
print(f"CPU навантаження: {info['cpu_load']}%")
print(f"RAM: {info['ram_used']}MB / {info['ram_total']}MB")
