import codecs
import configparser
from typing import List

from config import config
from modules.logs import get_logger

gui_logger = get_logger("gui")

INI_CONFIG_FILE_HEADER = "TF2-GPT-CHATBOT-CONFIG"
DROP_KEYS = ("APP_VERSION", "CONFIG_NAME", "HOST_USERNAME")


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


def save_config(filename: str):
    try:
        # Remove keys that are useless
        dict_ = {k: v for k, v in config.dict().items() if k not in DROP_KEYS}

        config_dict = {INI_CONFIG_FILE_HEADER: dict_}

        # Dump to a file
        parser = configparser.ConfigParser()
        parser.optionxform = str
        parser.read_dict(config_dict)
        with codecs.open(f"cfg/{filename}", "w", encoding="utf-8") as cfg_file:
            parser.write(cfg_file, space_around_delimiters=False)

        gui_logger.info("Config written successfully.")
    except Exception as e:
        gui_logger.warning(f"Failed to write config file [{e}]")


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
