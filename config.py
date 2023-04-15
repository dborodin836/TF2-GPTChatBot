import codecs
import configparser
import os
import sys
import re
from enum import IntEnum
from os.path import exists
from pydantic import BaseModel, validator

CONFIG_FILE = 'config.ini'
OPENAI_API_KEY_RE_PATTERN = r"sk-[a-zA-Z0-9]{48}"


def handle_exit_with_exception(message: str) -> None:
    print(message)
    os.system('pause')
    sys.exit(1)


class RTDModes(IntEnum):
    DISABLED = 0
    RICKROLL = 1
    RANDOM_MEME = 2

    @classmethod
    def has_value(cls, value):
        return value in {x.value for x in iter(RTDModes)}


if not exists(CONFIG_FILE):
    handle_exit_with_exception(f"Couldn't find '{CONFIG_FILE}' file.")

configparser_config = configparser.ConfigParser()
configparser_config.read(CONFIG_FILE)


class Config(BaseModel):
    TF2_LOGFILE_PATH: str
    OPENAI_API_KEY: str
    GPT_COMMAND: str
    CHATGPT_COMMAND: str
    CLEAR_CHAT_COMMAND: str
    RCON_HOST: str
    RCON_PASSWORD: str
    RCON_PORT: int
    SOFT_COMPLETION_LIMIT: int
    HARD_COMPLETION_LIMIT: int
    RTD_MODE: int

    @validator('OPENAI_API_KEY')
    def api_key_pattern_match(cls, v):
        if not re.fullmatch(OPENAI_API_KEY_RE_PATTERN, v):
            handle_exit_with_exception("API key not set or invalid! Check documentation and edit "
                                       "config.ini file.")
        return v

    @validator('RTD_MODE')
    def rtd_mode_is_valid_enum(cls, v):
        if not RTDModes.has_value(v):
            handle_exit_with_exception(
                f"Invalid RTD_MODE value! Expected one of {[mode.value for mode in RTDModes]}.")
        return v

    @validator('TF2_LOGFILE_PATH')
    def is_logfile_path_exists(cls, v):
        # if not os.path.exists(os.path.dirname(v)):
        #     handle_exit_with_exception(
        #         f"Non-valid logfile path!")
        #
        # if not os.path.exists(v):
        #     try:
        #
        #         with codecs.open(v, 'w', encoding='utf-8'):
        #             pass
        #     except Exception:
        #         handle_exit_with_exception(
        #             f"Non-valid logfile path!")
        print(1)
        return v


config: Config | None = Config(**{key.upper(): value for section in configparser_config.sections() for key, value
                   in
                   configparser_config.items(section)})


def init_config():
    config_dict = {key.upper(): value for section in configparser_config.sections() for key, value
                   in
                   configparser_config.items(section)}
    global config
    config = Config(**config_dict)
