import configparser
import os
import re
from enum import IntEnum
from os.path import exists

import pydantic
from pydantic import BaseModel, validator
from io import StringIO
import tkinter as tk
from tkinter import messagebox
import sys

CONFIG_FILE = 'config.ini'
OPENAI_API_KEY_RE_PATTERN = r"sk-[a-zA-Z0-9]{48}"
BUFFERED_CONFIG_INIT_LOG_MESSAGES = StringIO()


def buffered_print(message: str) -> None:
    BUFFERED_CONFIG_INIT_LOG_MESSAGES.write(message)


class RTDModes(IntEnum):
    DISABLED = 0
    RICKROLL = 1
    RANDOM_MEME = 2

    @classmethod
    def has_value(cls, value):
        return value in {x.value for x in iter(RTDModes)}


class Config(BaseModel):
    APP_VERSION: str = '1.2.0-hotfix1'
    HOST_USERNAME: str = ''

    TF2_LOGFILE_PATH: str
    OPENAI_API_KEY: str

    GPT_COMMAND: str
    CHATGPT_COMMAND: str
    CLEAR_CHAT_COMMAND: str
    RTD_COMMAND: str

    RCON_HOST: str
    RCON_PASSWORD: str
    RCON_PORT: int

    SOFT_COMPLETION_LIMIT: int
    HARD_COMPLETION_LIMIT: int

    RTD_MODE: int

    @validator('OPENAI_API_KEY')
    def api_key_pattern_match(cls, v):
        if not re.fullmatch(OPENAI_API_KEY_RE_PATTERN, v):
            buffered_print("API key not set or invalid! Check documentation and edit "
                           "config.ini file.")
        return v

    @validator('RTD_MODE')
    def rtd_mode_is_valid_enum(cls, v):
        if not RTDModes.has_value(v):
            buffered_print(
                f"Invalid RTD_MODE value! Expected one of {[mode.value for mode in RTDModes]}.")
        return v

    @validator('TF2_LOGFILE_PATH')
    def is_logfile_path_exists(cls, v):
        if not os.path.exists(os.path.dirname(v)):
            buffered_print(f"Non-valid logfile path!")
        return v


config: Config | None = None


def init_config():
    if not exists(CONFIG_FILE):
        buffered_print(f"Couldn't find '{CONFIG_FILE}' file.")

    try:
        configparser_config = configparser.ConfigParser()
        configparser_config.read(CONFIG_FILE)

        config_dict = {key.upper(): value for section in configparser_config.sections() for key, value
                       in
                       configparser_config.items(section)}
        global config
        config = Config(**config_dict)
    except pydantic.ValidationError:
        # Create a Tkinter window
        root = tk.Tk()
        root.withdraw()

        # Show error message
        messagebox.showerror("Error", "An error occurred. Check config file.")

        # Close the window
        root.destroy()
        sys.exit(1)
