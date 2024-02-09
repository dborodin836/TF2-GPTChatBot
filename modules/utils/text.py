import codecs
import os
import re
import time
import typing
from string import Template
from typing import Generator

from config import config
from modules.logs import get_logger
from modules.tf_statistics import StatsData
from modules.typing import LogLine, Player, Message
from modules.utils.prompts import PROMPTS
from modules.utils.time import get_minutes_from_str

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
            gui_logger.warning(f"Logfile doesn't exist. Checking again in 4 seconds.")
            time.sleep(4)
            yield ""
        except Exception as e:
            main_logger.error(f"Failed to parse line from game logfile [{e}]")
            yield ""


def parse_line(line: str) -> LogLine:
    if TF2BD_WRAPPER_FOLDER_EXIST:
        for char in TF2BD_WRAPPER_CHARS:
            line = line.replace(char, "")

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

    if len(parts) > 2:
        prompt = " ".join(parts[1:])
    else:
        prompt = parts[-1]

    return LogLine(prompt, username, is_team_mes)


def stats_regexes(line: str):
    # Parsing user line from status command
    if matches := re.search(
            r"^#\s*\d*\s*\"(.*)\"\s*(\[.*])\s*(\d*:?\d*:\d*)\s*(\d*)\s*\d*\s*\w*\s*\w*",
            line,
    ):
        time_on_server = matches.groups()[2]

        tm = get_minutes_from_str(time_on_server)

        d = Player(
            name=matches.groups()[0],
            minutes_on_server=tm,
            last_updated=tm,
            steamid3=matches.groups()[1],
            ping=matches.groups()[3],
        )

        StatsData.add_player(d)

    # Parsing map name on connection
    elif matches := re.search(r"^Map:\s(\w*)", line):
        map_ = matches.groups()[0]
        StatsData.set_map_name(map_)

    # Parsing server ip
    elif matches := re.search(r"^udp/ip\s*:\s*((\d*.){4}:\d*)", line):
        ip = matches.groups()[0]
        main_logger.info(f"Server ip is [{ip}]")
        StatsData.set_server_ip(ip)

    # Parsing kill
    elif matches := re.search(r"^(.*)\skilled\s(.*)\swith\s(\w*).", line):
        killer = matches.groups()[0]
        victim = matches.groups()[1]
        weapon = matches.groups()[2]
        is_crit = line.strip().endswith("(crit)")
        StatsData.process_kill(killer, victim, weapon, is_crit)

    # Parsing suicide
    elif matches := re.search(r"^(.*)\ssuicided", line):
        user = matches.groups()[0]
        StatsData.process_kill_bind(user)


def get_console_logline() -> typing.Generator:
    """
    Opens a log file for Team Fortress 2 and yields tuples containing user prompts and usernames.
    """
    for line in follow_tail(config.TF2_LOGFILE_PATH):
        # Remove timestamp
        line = line[23:]

        if config.ENABLE_STATS:
            stats_regexes(line)

        try:
            res = parse_line(line)
        except Exception as e:
            main_logger.warning(f"Unknown error happened while reading chat. [{e}]")
            res = LogLine("", "", False)
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
    args = prompt.split(" ")
    result = []

    # Get everything that starts with '\', stop when first item w/o '\' appears.
    for arg in args:
        if arg.startswith("\\"):
            result.append(arg)
        else:
            break

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


def get_system_message(user_prompt: str, enable_soft_limit: bool = True) -> Message:
    """
    Adds prompts to a user prompt based on the flags provided in the prompt.
    """
    args = get_args(user_prompt)
    message = ""

    for prompt in PROMPTS:
        if prompt["flag"] in args:
            message += prompt["prompt"]

    if r"\stats" in args and config.ENABLE_STATS:
        message = (
                f" {StatsData.get_data()} Based on this data answer following question. "
                + message
                + " Ignore unknown data."
        )

    if r"\l" not in args and enable_soft_limit:
        message += (
            f" Answer in less than {config.SOFT_COMPLETION_LIMIT} chars! {config.CUSTOM_PROMPT}"
        )

    return Message(role="system", content=message)
