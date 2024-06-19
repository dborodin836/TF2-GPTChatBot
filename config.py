import configparser
import json
import os
import re
from enum import IntEnum
from os.path import exists
from typing import Any, Dict, Optional

from pydantic import BaseModel, ValidationError, field_validator

from modules.utils.buffered_messages import buffered_fail_message, buffered_message

DEFAULT_CONFIG_FILE = "config.ini"
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
    config_file = filename or DEFAULT_CONFIG_FILE
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

    # Set loaded config filename
    config_dict["CONFIG_NAME"] = config_file

    return config_dict


class Config(BaseModel):
    """
    May only contain validators that do not raise Exceptions and fields.
    """

    # App Internals
    APP_VERSION: str = "1.4.0"
    CONFIG_NAME: str = "config.ini"

    # Player stuff
    HOST_USERNAME: str = ""
    HOST_STEAMID3: str = "[U:X:XXXXXXX]"

    # Required
    TF2_LOGFILE_PATH: str = (
        r"C:\Program Files (x86)\Steam\steamapps\common\Team Fortress 2\tf\console.log"
    )

    # RCON
    RCON_HOST: str = "127.0.0.1"
    RCON_PASSWORD: str = "password"
    RCON_PORT: int = 42465

    # OpenAI
    OPENAI_API_KEY: str = "sk-" + "X" * 48

    # Text Generation Web UI
    CUSTOM_MODEL_HOST: str = "127.0.0.1"

    # GroqCloud
    GROQ_API_KEY: str = "gsk_" + "X" * 52

    # Chat
    DELAY_BETWEEN_MESSAGES: float = 1.3
    CLEAR_CHAT_COMMAND: str = "!clear"
    ENABLE_SHORTENED_USERNAMES_RESPONSE: bool = True
    SHORTENED_USERNAMES_FORMAT: str = "[$username] "
    SHORTENED_USERNAME_LENGTH: int = 12

    # Roll the Dice
    RTD_COMMAND: str = "!rtd"
    RTD_MODE: int = RTDModes.DISABLED

    # Misc
    DISABLE_KEYBOARD_BINDINGS: bool = False
    FALLBACK_TO_USERNAME: bool = False

    # Stats
    STEAM_WEBAPI_KEY: str = "X" * 32
    ENABLE_STATS_LOGS: bool = False

    # Experimental
    CONFIRMABLE_QUEUE: bool = False

    def load_from_file(self, filename: str) -> None:
        config_dict = read_config_from_file(filename)

        for k, v in config_dict.items():
            self.__setattr__(k, v)


class ValidatableConfig(Config):
    """
    Should only contain validators.
    """

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


def init_config(filename: Optional[str] = None) -> Dict[str, Any]:
    # Get config file location
    # TODO: redo with pathlib
    config_file = filename or DEFAULT_CONFIG_FILE
    config_file_path = "cfg/" + config_file

    # Check if file exists.
    if not exists(config_file_path):
        buffered_fail_message("Config file is missing.", "LOG", level="ERROR")
        buffered_fail_message(
            f"Couldn't find '{config_file_path}' file.", type_="BOTH", level="ERROR"
        )

    # Parse config file
    buffered_message("Starting parsing config file.", "LOG", level="INFO")
    configparser_config = configparser.ConfigParser()
    configparser_config.read(config_file_path, encoding="utf-8")

    # Make dict with UPPERCASE keys out of parsed config
    config_dict: dict[str, str | None] = {
        key.upper(): value
        for section in configparser_config.sections()
        for key, value in configparser_config.items(section)
    }

    # Set loaded config filename
    config_dict["CONFIG_NAME"] = config_file

    return config_dict


def get_formatter_errors(exc: ValidationError) -> str:
    rtn: str = ""
    rtn += f"Found {exc.error_count()} error(s)!\n"
    for err in exc.errors():
        # If loc key is missing replace it with ERR_UNKNOWN_OPTION string
        loc = err.get("loc", ("ERR_UNKNOWN_OPTION",))[0]
        rtn += f"{loc}\n\t{err.get('msg')}"
    rtn += "\n"
    return rtn


def load_config() -> Config:
    # Attempt #1: Load the initial config
    try:
        return ValidatableConfig(**init_config())
    except ValidationError as exc:
        buffered_fail_message("#############################", "GUI", level="WARNING")
        buffered_fail_message("#  Config file is invalid.  #", "GUI", level="WARNING")
        buffered_fail_message("#############################", "GUI", level="WARNING")
        buffered_message(f"{get_formatter_errors(exc)}", "GUI", level="WARNING")

    # Attempt #2: Load the config anyway so user can edit it
    try:
        return Config(**init_config())
    except Exception as exc:
        buffered_fail_message(
            "Failed to load config. Loading default config...", "BOTH", level="ERROR"
        )
        buffered_fail_message(
            "Failed to load config. Loading default config.", "BOTH", level="ERROR"
        )

    # Attempt #3: Load a default config as a last resort
    return Config()


class ConfigWrapper:
    def __init__(self):
        self.__dict__["_config"]: Config = load_config()

    def update_config(self, config: Config):
        self.__dict__["_config"] = config

    def __getattr__(self, name):
        return getattr(self._config, name)

    def __setattr__(self, name, value):
        setattr(self._config, name, value)


config: ConfigWrapper = ConfigWrapper()
