import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from optimizer.system_info import get_system_info

def main():
    print("=== System Information ===")
    info = get_system_info()

    for key, value in info.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    main()
