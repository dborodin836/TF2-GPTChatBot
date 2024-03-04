from typing import List

from config import config
from modules.logs import get_logger

gui_logger = get_logger("gui")


def reload_config():
    try:
        config.load_from_file(config.CONFIG_NAME)
        gui_logger.info("Config reloaded successfully.")
    except Exception as e:
        gui_logger.warning(f"Failed to reload config file [{e}]")


def load_config(filename: str):
    try:
        config.load_from_file(filename)
        gui_logger.info("Config loaded successfully.")
    except Exception as e:
        gui_logger.warning(f"Failed to load config file [{e}]")


def save_config():
    ...


def set_value_config(values: List):
    for item in values:
        name, val = item
        try:
            config.__setattr__(name, val)
            gui_logger.info(f"Setting {name} was set.")
        except KeyError:
            gui_logger.info(f"Setting {name} doesn't exist.")
        except Exception as e:
            gui_logger.warning(f"Error occurred [{e}]")


def get_value_config(values: List):
    for val in values:
        try:
            result = config.dict()[val]
            gui_logger.info(f"{val}={result}")
        except KeyError:
            gui_logger.warning(f"Setting {val} doesn't exist.")
        except Exception as e:
            gui_logger.warning(f"Error occurred [{e}]")
