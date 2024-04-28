import configparser
import json
import os
import re
import sys
import tkinter as tk
from enum import IntEnum
from os.path import exists
from tkinter import messagebox
from typing import Optional

import pydantic
from pydantic import BaseModel, validator

from modules.utils.buffered_messages import buffered_fail_message, buffered_message

CONFIG_FILE = "config.ini"
OPENAI_API_KEY_RE_PATTERN = r"sk-[a-zA-Z0-9]{48}"
WEB_API_KEY_RE_PATTERN = r"[a-zA-Z0-9]{32}"


class RTDModes(IntEnum):
    DISABLED = 0
    RICKROLL = 1
    RANDOM_MEME = 2

    @classmethod
    def has_value(cls, value):
        return value in {x.value for x in iter(RTDModes)}


class Config(BaseModel):
    APP_VERSION: str = "1.3.0"
    HOST_USERNAME: str = ""
    HOST_STEAMID3: str = "[U:X:XXXXXXX]"
    TOS_VIOLATION: bool
    FALLBACK_TO_USERNAME: bool

    TF2_LOGFILE_PATH: str
    OPENAI_API_KEY: str

    STEAM_WEBAPI_KEY: str
    DISABLE_KEYBOARD_BINDINGS: bool
    GPT4_COMMAND: str
    GPT4_LEGACY_COMMAND: str

    ENABLE_OPENAI_COMMANDS: bool
    GPT3_MODEL: str
    GPT3_CHAT_MODEL: str
    GPT4_MODEL: str
    GPT4L_MODEL: str

    GPT_COMMAND: str
    CHATGPT_COMMAND: str
    CLEAR_CHAT_COMMAND: str
    RTD_COMMAND: str
    GLOBAL_CHAT_COMMAND: str
    GPT4_ADMIN_ONLY: bool
    ENABLE_STATS_LOGS: bool

    CUSTOM_PROMPT: str

    RCON_HOST: str
    RCON_PASSWORD: str
    RCON_PORT: int

    SOFT_COMPLETION_LIMIT: int
    HARD_COMPLETION_LIMIT: int
    ENABLE_SHORTENED_USERNAMES_RESPONSE: bool
    SHORTENED_USERNAMES_FORMAT: str
    SHORTENED_USERNAME_LENGTH: int
    DELAY_BETWEEN_MESSAGES: float
    ENABLE_SOFT_LIMIT_FOR_CUSTOM_MODEL: bool

    RTD_MODE: int

    ENABLE_CUSTOM_MODEL: bool
    CUSTOM_MODEL_HOST: str
    CUSTOM_MODEL_COMMAND: str
    CUSTOM_MODEL_CHAT_COMMAND: str
    GLOBAL_CUSTOM_CHAT_COMMAND: str
    GREETING: str

    CONFIRMABLE_QUEUE: bool

    CUSTOM_MODEL_SETTINGS: Optional[str | dict]

    GROQ_API_KEY: str
    GROQ_COMMAND: str
    GROQ_CHAT_COMMAND: str
    GROQ_PRIVATE_CHAT: str
    GROQ_MODEL: str
    GROQ_ENABLE: bool

    @validator("OPENAI_API_KEY")
    def api_key_pattern_match(cls, v):
        if not re.fullmatch(OPENAI_API_KEY_RE_PATTERN, v):
            buffered_fail_message("API key not set or invalid!", type_="BOTH", level="ERROR")
        return v

    @validator("STEAM_WEBAPI_KEY")
    def steam_webapi_key_pattern_match(cls, v, values):
        if not re.fullmatch(WEB_API_KEY_RE_PATTERN, v):
            buffered_fail_message(
                "STEAM WEB API key not set or invalid!", type_="BOTH", level="ERROR"
            )
        return v

    @validator("SHORTENED_USERNAMES_FORMAT")
    def is_username_in_template_string(cls, v):
        if not "$username" in v:
            buffered_fail_message(
                f"'SHORTENED_USERNAMES_FORMAT' setting does not contain '$username' ({v}).",
                type_="BOTH",
                level="ERROR",
            )
        return v

    @validator("RTD_MODE")
    def rtd_mode_is_valid_enum(cls, v):
        if not RTDModes.has_value(v):
            buffered_fail_message(
                f"Invalid RTD_MODE value! Expected one of {[mode.value for mode in RTDModes]}.",
                type_="BOTH",
                level="ERROR",
            )
        return v

    @validator("TF2_LOGFILE_PATH")
    def is_logfile_path_exists(cls, v):
        if not os.path.exists(os.path.dirname(v)):
            buffered_fail_message("Non-valid logfile path!", type_="BOTH", level="ERROR")
        return v


config: Optional[Config] = None


def show_error_window(err):
    # Create a Tkinter window
    root = tk.Tk()
    root.withdraw()

    # Show error message
    messagebox.showerror("Error", f"An error occurred. Check config file. [{err}]")

    # Close the window
    root.destroy()
    sys.exit(1)


def init_config():
    if not exists(CONFIG_FILE):
        buffered_fail_message("Config file is missing.", "LOG", level="ERROR")
        buffered_fail_message(f"Couldn't find '{CONFIG_FILE}' file.", type_="BOTH", level="ERROR")

    try:
        buffered_message("Starting parsing config file.", "LOG", level="INFO")
        configparser_config = configparser.ConfigParser()
        configparser_config.read(CONFIG_FILE, encoding="utf-8")

        config_dict: dict[str, str | None] = {
            key.upper(): value
            for section in configparser_config.sections()
            for key, value in configparser_config.items(section)
        }
        global config
        try:
            if config_dict.get("CUSTOM_MODEL_SETTINGS") != "":
                config_dict["CUSTOM_MODEL_SETTINGS"] = json.loads(
                    config_dict.get("CUSTOM_MODEL_SETTINGS")
                )
        except Exception as e:
            buffered_fail_message(
                f"CUSTOM_MODEL_SETTINGS is not dict [{e}].", "BOTH", level="ERROR"
            )

        config = Config(**config_dict)

        if not config.ENABLE_OPENAI_COMMANDS and not config.ENABLE_CUSTOM_MODEL:
            buffered_message("You haven't enabled any AI related commands.")

    except (pydantic.ValidationError, Exception) as e:
        show_error_window(e)
