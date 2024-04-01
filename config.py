import configparser
import json
import os
import re
from enum import IntEnum
from os.path import exists
from typing import Dict, Optional

from pydantic import BaseModel, field_validator

from modules.utils.buffered_messages import buffered_fail_message, buffered_message

DEAFAULT_CONFIG_FILE = "config.ini"
OPENAI_API_KEY_RE_PATTERN = r"sk-[a-zA-Z0-9]{48}"
WEB_API_KEY_RE_PATTERN = r"[a-zA-Z0-9]{32}"


class RTDModes(IntEnum):
    DISABLED = 0
    RICKROLL = 1
    RANDOM_MEME = 2

    @classmethod
    def has_value(cls, value):
        return value in {x.value for x in iter(RTDModes)}


def read_config_from_file(filename: str) -> Dict:
    config_file = filename or DEAFAULT_CONFIG_FILE
    # TODO: redo with pathlib
    config_file_path = "cfg/" + config_file

    if not exists(config_file_path):
        raise Exception("File doesn't exist.")

    configparser_config = configparser.ConfigParser()
    configparser_config.read(config_file_path, encoding="utf-8")

    config_dict: dict[str, str | None] = {
        key.upper(): value
        for section in configparser_config.sections()
        for key, value in configparser_config.items(section)
    }

    try:
        if config_dict.get("CUSTOM_MODEL_SETTINGS") != "":
            key = config_dict.get("CUSTOM_MODEL_SETTINGS")
            if key is None:
                key = ""
            config_dict["CUSTOM_MODEL_SETTINGS"] = json.loads(key)
    except Exception as e:
        raise Exception(f"CUSTOM_MODEL_SETTINGS is not dict [{e}].")

    # Set loaded config filename
    config_dict["CONFIG_NAME"] = config_file

    return config_dict


class Config(BaseModel):
    APP_VERSION: str = "1.3.0"
    CONFIG_NAME: str = "config.ini"
    HOST_USERNAME: str = ""
    HOST_STEAMID3: str = "[U:X:XXXXXXX]"
    TOS_VIOLATION: bool = False
    FALLBACK_TO_USERNAME: bool = False

    TF2_LOGFILE_PATH: str = (
        r"C:\Program Files (x86)\Steam\steamapps\common\Team Fortress 2\tf\console.log"
    )
    OPENAI_API_KEY: str = "sk-" + "X" * 48

    STEAM_WEBAPI_KEY: str = "X" * 32
    DISABLE_KEYBOARD_BINDINGS: bool = False
    GPT4_COMMAND: str = "!gpt4"
    GPT4_LEGACY_COMMAND: str = "!gpt4l"

    ENABLE_OPENAI_COMMANDS: bool = True
    GPT3_MODEL: str = "gpt-3.5-turbo"
    GPT3_CHAT_MODEL: str = "gpt-3.5-turbo"
    GPT4_MODEL: str = "gpt-4-1106-preview"
    GPT4L_MODEL: str = "gpt-4"

    GPT_COMMAND: str = "!gpt3"
    CHATGPT_COMMAND: str = "!pc"
    CLEAR_CHAT_COMMAND: str = "!clear"
    RTD_COMMAND: str = "!rtd"
    GLOBAL_CHAT_COMMAND: str = "!cgpt"
    GPT4_ADMIN_ONLY: bool = False
    ENABLE_STATS_LOGS: bool = False

    CUSTOM_PROMPT: str = ""

    RCON_HOST: str = "127.0.0.1"
    RCON_PASSWORD: str = "password"
    RCON_PORT: int = 42465

    SOFT_COMPLETION_LIMIT: int = 128
    HARD_COMPLETION_LIMIT: int = 300
    ENABLE_SHORTENED_USERNAMES_RESPONSE: bool = True
    SHORTENED_USERNAMES_FORMAT: str = "[$username] "
    SHORTENED_USERNAME_LENGTH: int = 12
    DELAY_BETWEEN_MESSAGES: float = 1.3
    ENABLE_SOFT_LIMIT_FOR_CUSTOM_MODEL: bool = True

    RTD_MODE: int = RTDModes.DISABLED

    ENABLE_CUSTOM_MODEL: bool = False
    CUSTOM_MODEL_HOST: str = "127.0.0.1"
    CUSTOM_MODEL_COMMAND: str = "!ai"
    CUSTOM_MODEL_CHAT_COMMAND: str = "!pcc"
    GLOBAL_CUSTOM_CHAT_COMMAND: str = "!chat"
    GREETING: str = ""

    CONFIRMABLE_QUEUE: bool = False

    CUSTOM_MODEL_SETTINGS: Optional[str | dict] = {}

    def load_from_file(self, filename: str) -> None:
        config_dict = read_config_from_file(filename)

        for k, v in config_dict.items():
            self.__setattr__(k, v)

    @field_validator("OPENAI_API_KEY")
    def api_key_pattern_match(cls, v):
        if not re.fullmatch(OPENAI_API_KEY_RE_PATTERN, v):
            raise ValueError("API key not set or invalid!")
        return v

    @field_validator("STEAM_WEBAPI_KEY")
    def steam_webapi_key_pattern_match(cls, v):
        if not re.fullmatch(WEB_API_KEY_RE_PATTERN, v):
            raise ValueError("STEAM WEB API key not set or invalid!")
        return v

    @field_validator("SHORTENED_USERNAMES_FORMAT")
    def is_username_in_template_string(cls, v):
        if "$username" not in v:
            raise ValueError(
                f"'SHORTENED_USERNAMES_FORMAT' setting does not contain '$username' ({v})."
            )
        return v

    @field_validator("RTD_MODE")
    def rtd_mode_is_valid_enum(cls, v):
        if not RTDModes.has_value(v):
            raise ValueError(
                f"Invalid RTD_MODE value! Expected one of {[mode.value for mode in RTDModes]}."
            )
        return v

    @field_validator("TF2_LOGFILE_PATH")
    def is_logfile_path_exists(cls, v):
        if not os.path.exists(os.path.exists(v)):
            raise ValueError("Invalid logfile path!")
        return v


def init_config(filename: Optional[str] = None) -> Config:
    config_file = filename or DEAFAULT_CONFIG_FILE
    # TODO: redo with pathlib
    config_file_path = "cfg/" + config_file

    if not exists(config_file_path):
        buffered_fail_message("Config file is missing.", "LOG", level="ERROR")
        buffered_fail_message(
            f"Couldn't find '{config_file_path}' file.", type_="BOTH", level="ERROR"
        )

    buffered_message("Starting parsing config file.", "LOG", level="INFO")
    configparser_config = configparser.ConfigParser()
    configparser_config.read(config_file_path, encoding="utf-8")

    config_dict: dict[str, str | None] = {
        key.upper(): value
        for section in configparser_config.sections()
        for key, value in configparser_config.items(section)
    }
    try:
        if config_dict.get("CUSTOM_MODEL_SETTINGS") != "":
            val = config_dict.get("CUSTOM_MODEL_SETTINGS")
            if val:
                config_dict["CUSTOM_MODEL_SETTINGS"] = json.loads(val)
            else:
                raise Exception
    except Exception as e:
        buffered_fail_message(f"CUSTOM_MODEL_SETTINGS is not dict [{e}].", "BOTH", level="ERROR")

    # Set loaded config filename
    config_dict["CONFIG_NAME"] = config_file

    config = Config(**config_dict)  # type: ignore[arg-type]

    if not config.ENABLE_OPENAI_COMMANDS and not config.ENABLE_CUSTOM_MODEL:
        buffered_message("You haven't enabled any AI related commands.")

    return config


try:
    config: Config = init_config()
except Exception as e:
    buffered_fail_message(f"#############################", "GUI", level="INFO")
    buffered_fail_message(f"#  Config file is invalid.  #", "GUI", level="INFO")
    buffered_fail_message(f"#############################", "GUI", level="INFO")
    buffered_message(f"{e}", "BOTH", level="INFO")
    config = Config()
