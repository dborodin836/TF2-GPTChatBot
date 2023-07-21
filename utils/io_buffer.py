import os
from io import StringIO

from config import BUFFERED_CONFIG_INIT_LOG_MESSAGES


def get_io_string_size(string_io: StringIO) -> int:
    """
    Calculate the number of string stored within a StringIO object.
    """
    string_io.seek(0, os.SEEK_END)
    length = string_io.tell()
    string_io.seek(0)
    return length


def print_buffered_config_innit_messages() -> None:
    """
    Prints the initialization messages saved in the BUFFERED_CONFIG_INIT_LOG_MESSAGES buffer.
    """
    BUFFERED_CONFIG_INIT_LOG_MESSAGES.seek(0)

    if get_io_string_size(BUFFERED_CONFIG_INIT_LOG_MESSAGES) > 0:
        for line in BUFFERED_CONFIG_INIT_LOG_MESSAGES:
            print(line, end='\n')
    else:
        print("Config file looks good!")
