import sys
sys.path.insert(0, '.')
from src.optimizer.system_info import get_system_info

result = get_system_info()
print(result)
