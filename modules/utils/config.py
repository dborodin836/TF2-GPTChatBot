import codecs
import configparser
import pprint
from typing import List

import yaml

from config import config
from modules.logs import get_logger

gui_logger = get_logger("gui")

INI_CONFIG_FILE_HEADER = "TF2-GPT-CHATBOT-CONFIG"
DROP_KEYS = ("APP_VERSION", "CONFIG_NAME", "HOST_USERNAME", "HOST_STEAMID3")


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

        # Replace None values with empty string
        for k, v in dict_.items():
            if v is None:
                dict_[k] = ""

        # Add header
        config_dict = {INI_CONFIG_FILE_HEADER: dict_}

        # Dump to a file
        parser = configparser.ConfigParser()
        parser.optionxform = str  # type: ignore[method-assign,assignment]
        parser.read_dict(config_dict)
        with codecs.open(f"cfg/{filename}", "w", encoding="utf-8") as cfg_file:
            parser.write(cfg_file, space_around_delimiters=False)

        gui_logger.info("Config written successfully.")
    except Exception as e:
        gui_logger.warning(f"Failed to write config file [{e}]")


def save_commands(data):
    with codecs.open("cfg/commands.yaml", "w", encoding="utf-8") as file:
        yaml.dump(data, file)


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


def dump_config():
    string = pprint.pformat(config.dict(), indent=2, width=180)
    gui_logger.info(string)
