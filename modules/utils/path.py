import os
import sys

from modules.logs import get_logger

main_logger = get_logger("main")


def resource_path(relative_path: str):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception as e:
        main_logger.warning(f"Running from source. [{e}]")
        base_path = os.path.abspath("")

    return os.path.join(base_path, relative_path)
