import codecs
import os
import re
import time
import typing
from string import Template
from typing import Generator

from config import config
from modules.lobby_manager import lobby_manager
from modules.logs import get_logger
from modules.rcon_client import RconClient
from modules.typing import LogLine, Message
from modules.utils.prompts import PROMPTS

main_logger = get_logger("main")
gui_logger = get_logger("gui")

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
try:
    TF2BD_WRAPPER_FOLDER_EXIST = os.path.exists(
        os.path.join(
            os.path.dirname(config.TF2_LOGFILE_PATH),
            "custom/aaaaaaaaaa_loadfirst_tf2_bot_detector",
        )
    )
except AttributeError:
    # Nothing bad will happen if we set this to True
    main_logger.warning(f"Attribute error while checking for TF2BD wrapper.")
    TF2BD_WRAPPER_FOLDER_EXIST = True
except Exception as e:
    main_logger.error(f"Failed to check for TF2BD wrapper. [{e}]")
    TF2BD_WRAPPER_FOLDER_EXIST = True


def split_into_chunks(string: str, maxlength: int) -> typing.Generator:
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


def follow_tail(file_path: str) -> typing.Generator:
    """
    Follows the tail of a file, yielding new lines as they are added.
    """
    first_call = True
    while True:
        try:
            with codecs.open(file_path, encoding="utf-8", errors="ignore") as input:
                if first_call:
                    input.seek(0, 2)
                    first_call = False
                latest_data = input.read()
                while True:
                    if "\n" not in latest_data:
                        latest_data += input.read()
                        if "\n" not in latest_data:
                            yield ""
                            if not os.path.isfile(file_path):
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


def parse_line(line: str) -> typing.Optional[LogLine]:
    # Fixes issue #80
    # Valve servers use 2 spaces after the colon symbol, but some servers use one.
    # Default:                          Modified:
    # <username>_:__<message>           <username>_:_<message>
    if " :  " in line:
        parts = line.split(" :  ")
    else:
        parts = line.split(" : ")

    is_team_mes = "(TEAM)" in line
    username = parts[0].replace("(TEAM)", "", 1).removeprefix("*DEAD*").strip()

    if username == "":
        return None

    if not lobby_manager.is_username_exist(username):
        username = lobby_manager.search_username(username)

    player = lobby_manager.get_player_by_name(username)
    if player is None:
        main_logger.trace(f"Player with username '{username}' not found.")
        return None

    if len(parts) > 2:
        prompt = " ".join(parts[1:])
    else:
        prompt = parts[-1]

    return LogLine(prompt, username, is_team_mes, player)


ever_updated: bool = False
last_updated: float = 0.0
max_delay: float = 20
min_delay: float = 10


def get_console_logline() -> typing.Generator:
    """
    Opens a log file for Team Fortress 2 and yields tuples containing user prompts and usernames.
    """
    global last_updated, ever_updated

    for line in follow_tail(config.TF2_LOGFILE_PATH):
        # Remove timestamp
        line: str = line[23:]

        # Remove TF2BD chars
        if TF2BD_WRAPPER_FOLDER_EXIST:
            for char in TF2BD_WRAPPER_CHARS:
                line = line.replace(char, "").strip()

        # Send status commands based on events
        if "Lobby updated" in line:
            if time.time() - last_updated > min_delay:
                main_logger.debug("Sending status command on lobby update connection.")
                last_updated = time.time()
                get_status()

        if line.endswith("connected"):
            if time.time() - last_updated > min_delay:
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
        if lobby_manager.stats_regexes(line):
            ever_updated = True
            continue

        res = None

        try:
            res = parse_line(line)
        except Exception as e:
            main_logger.warning(f"Unknown error happened while reading chat. [{e}]")
        finally:
            yield res


def get_chunks(message: str) -> Generator:
    chunks_size: int = get_chunk_size(message)
    chunks = split_into_chunks(" ".join(message.split()), chunks_size)
    return chunks


def remove_hashtags(text: str) -> str:
    """
    Removes hashtags from a given string.
    """
    cleaned_text = re.sub(r"#\w+", "", text).strip()
    return cleaned_text


def get_args(prompt: str) -> typing.List[str]:
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
    message = prompt.split(" ")
    result = []
    args_ended = False

    for item in message:
        if item.startswith("\\") and not args_ended:
            continue
        else:
            result.append(item)

    return " ".join(result)


def get_status():
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
