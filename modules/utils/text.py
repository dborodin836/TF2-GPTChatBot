import codecs
import os
import re
import time
import typing
from string import Template
from typing import Generator, Optional

from config import config
from modules.lobby_manager import lobby_manager
from modules.logs import gui_logger, main_logger
from modules.rcon_client import RconClient
from modules.typing import GameChatMessage

MAX_LENGTH_CYRILLIC = 65
MAX_LENGTH_OTHER = 120

TF2BD_WRAPPER_CHARS = [
    "\u200e",
    "\u200d",
    "\ufeff",
    "\u200b",
    "\u200f",
    "\u202c",
    "\u2060",
    "\u200c",
]


def split_into_chunks(string: str, maxlength: int) -> typing.Generator[str, None, None]:
    """
    This function splits a string into chunks of a maximum length, with each chunk ending at the
    last space character before the maximum length.
    """
    start = 0
    end = 0
    while start + maxlength < len(string) and end != -1:
        end = string.rfind(" ", start, start + maxlength + 1)
        yield string[start:end]
        start = end + 1
    yield string[start:]


def get_shortened_username(username: str) -> str:
    """
    Shortens the given username if it exceeds a predefined length and formats it using a template.
    """
    template = Template(config.SHORTENED_USERNAMES_FORMAT)

    if len(username) > config.SHORTENED_USERNAME_LENGTH:
        username = username[: config.SHORTENED_USERNAME_LENGTH] + ".."

    try:
        result = template.safe_substitute(username=username)
    except Exception as e:
        main_logger.error(f"Failed to substitute template [{e}].")
        result = ""

    return result


def has_cyrillic(text: str) -> bool:
    """
    Checks if a string contains any Cyrillic characters.
    """
    return bool(re.search("[а-яА-Я]", text))


def get_chunk_size(text: str) -> int:
    """
    This function determines the maximum chunk size based on whether the input text contains
    Cyrillic characters or not.
    """
    if has_cyrillic(text):
        return MAX_LENGTH_CYRILLIC
    return MAX_LENGTH_OTHER


def follow_tail() -> Generator[str, None, None]:
    """
    Follows the tail of a file, yielding new lines as they are added.
    """
    first_call = True
    while True:
        try:
            with codecs.open(config.TF2_LOGFILE_PATH, encoding="utf-8", errors="ignore") as input:
                if first_call:
                    input.seek(0, 2)
                    first_call = False
                latest_data = input.read()
                while True:
                    if "\n" not in latest_data:
                        latest_data += input.read()
                        if "\n" not in latest_data:
                            yield ""
                            if not os.path.isfile(config.TF2_LOGFILE_PATH):
                                break
                            time.sleep(0.1)
                            continue
                    latest_lines = latest_data.split("\n")
                    if latest_data[-1] != "\n":
                        latest_data = latest_lines[-1]
                    else:
                        latest_data = input.read()
                    for line in latest_lines[:-1]:
                        yield line + "\n"
        except FileNotFoundError:
            gui_logger.warning("Logfile doesn't exist. Checking again in 4 seconds.")
            time.sleep(4)
            yield ""
        except Exception as e:
            main_logger.error(f"Failed to parse line from game logfile [{e}]")
            yield ""


def try_parse_chat_message(logline: str) -> Optional[GameChatMessage]:
    """
    Tries to parse a chat message from a logline.
    """

    # Fixes issue #80
    # Valve servers use 2 spaces after the colon symbol, but some servers use one.
    # Default:                          Modified:
    # <username>_:__<message>           <username>_:_<message>
    if " :  " in logline:
        parts = logline.split(" :  ")
    else:
        parts = logline.split(" : ")

    is_team_mes = "(TEAM)" in logline
    username = parts[0].replace("(TEAM)", "", 1).removeprefix("*DEAD*").strip()

    # Username can't be empty
    if username == "":
        return None

    # Check if the username exists, if not, try to search for it.
    if not lobby_manager.is_username_exist(username):
        username = lobby_manager.search_username(username)

    # Get the player object
    player = lobby_manager.get_player_by_name(username)
    if player is None:
        main_logger.trace(f"Player with username '{username}' not found.")
        return None

    # Join all parts of the message, if more than 2 are found.
    if len(parts) > 2:
        chat_msg = " ".join(parts[1:])
    else:
        chat_msg = parts[-1]

    return GameChatMessage(chat_msg, username, is_team_mes, player)


ever_updated: bool = False
last_updated: float = 0.0
max_delay: float = 20
min_delay: float = 10


def parse_logline_and_yield_chat_message() -> Generator[GameChatMessage, None, None]:
    """
    Parse log lines and yields chat messages if they are successfully parsed.
    It also handles sending status commands based on certain events.
    """
    global last_updated, ever_updated

    for log_line in follow_tail():
        # Remove timestamp
        log_line = log_line[23:]

        # Remove TF2BD chars
        for char in TF2BD_WRAPPER_CHARS:
            log_line = log_line.replace(char, "").strip()

        # Send status commands based on events
        if "Lobby updated" in log_line and time.time() - last_updated > min_delay:
            main_logger.debug("Sending status command on lobby update connection.")
            last_updated = time.time()
            get_status()

        if log_line.endswith("connected") and time.time() - last_updated > min_delay:
            main_logger.debug("Sending status command on new player connection.")
            last_updated = time.time()
            get_status()

        if time.time() - last_updated > max_delay:
            main_logger.debug("Max delay between status commands exceeded.")
            last_updated = time.time()
            get_status()

        if not ever_updated:
            get_status()

        # Ignore if line is from status command output
        if lobby_manager.parse_stats_regex(log_line):
            ever_updated = True
            continue

        try:
            chat_message = try_parse_chat_message(log_line)
            if chat_message is not None:
                yield chat_message
        except Exception as e:
            main_logger.warning(f"Unknown error happened while reading chat. [{e}]")


def get_chunks(string: str) -> Generator[str, None, None]:
    """
    This function takes a string as input and generates chunks of the string.
    """
    chunks_size: int = get_chunk_size(string)
    chunks = split_into_chunks(" ".join(string.split()), chunks_size)
    return chunks


def remove_hashtags(string: str) -> str:
    """
    Removes hashtags from a given string.
    """
    cleaned_text = re.sub(r"#\w+", "", string).strip()
    return cleaned_text


def get_args(prompt: str) -> typing.List[str]:
    """
    Parse the input string and extract arguments while considering quotes and escape characters.
    """
    in_quote = None  # Track the type of quote we're inside (None, single ', or double ")
    current_arg = ""
    result = []
    escape_next = False  # Flag to indicate the next character is escaped

    for char in prompt:
        if escape_next:
            current_arg += char
            escape_next = False
        elif char == "\\":  # Detect backslash
            if current_arg and not current_arg.startswith("\\"):
                # If current_arg doesn't start with \, reset it. Prepare for new arg.
                current_arg = char
            else:
                if not in_quote:
                    # If not in a quote, handle correctly as start of new arg or part of escaping
                    if current_arg:
                        result.append(current_arg)
                        current_arg = char
                    else:
                        current_arg += char
                else:
                    # Inside quotes, just add it
                    current_arg += char
        elif char in ['"', "'"]:  # Toggle in_quote state for both ' and "
            if char == in_quote:  # Exiting the quote
                in_quote = None
            elif not in_quote:  # Entering a quote
                in_quote = char
            current_arg += char
        elif char == " " and not in_quote:
            if current_arg:
                if current_arg.startswith("\\"):  # Ensure arg starts with a backslash
                    result.append(current_arg)
                current_arg = ""
        else:
            current_arg += char

    if current_arg and current_arg.startswith("\\"):  # Check for the last argument
        result.append(current_arg)

    return result


def remove_args(prompt: str) -> str:
    """
    Function to remove arguments from a given prompt string.
    """
    message = prompt.split(" ")
    result = []
    args_ended = False

    for item in message:
        if item.startswith("\\") and not args_ended:
            continue
        else:
            result.append(item)

    return " ".join(result)


def get_status() -> str:
    """
    Get the status by running a command through Rcon.
    """
    while True:
        try:
            with RconClient() as client:
                return client.run("cmd status")
        except ConnectionRefusedError:
            main_logger.warning("Failed to fetch status. Connection refused!")
            time.sleep(2)
        except Exception as e:
            main_logger.warning(f"Failed to fetch status. [{e}]")
            time.sleep(2)
