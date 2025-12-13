from src.tests import test_system_info
from src.tests import test_fps_booster
from src.tests import test_cleaner
from src.tests import test_advanced_cleaner

def main():
    print("=== RUNNING TESTS ===")
    test_system_info.run_tests()
    test_fps_booster.run_tests()
    test_cleaner.run_tests()
    test_advanced_cleaner.run_tests()
    print("=== ALL TESTS PASSED ===")


if __name__ == "__main__":
    main()
