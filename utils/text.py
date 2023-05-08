import codecs
import re
import os
import time
import typing

from config import config
from utils.prompt import PROMPTS
from utils.types import LogLine

MAX_LENGTH_CYRILLIC = 65
MAX_LENGTH_OTHER = 120


def get_chunks(string: str, maxlength: int) -> typing.Generator:
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


def has_cyrillic(text: str) -> bool:
    """
    Checks if a string contains any Cyrillic characters.
    """
    return bool(re.search('[а-яА-Я]', text))


def get_chunk_size(text: str) -> int:
    """
    This function determines the maximum chunk size based on whether the input text contains
    Cyrillic characters or not.
    """
    if has_cyrillic(text):
        return MAX_LENGTH_CYRILLIC
    return MAX_LENGTH_OTHER


def add_prompts_by_flags(user_prompt: str) -> str:
    """
    Adds prompts to a user prompt based on the flags provided in the prompt.
    """
    #  This args var also contains user prompt lul
    args = user_prompt.split(' ')
    result = ''

    for item in PROMPTS:
        if item["flag"] in args:
            result += item["prompt"]
            user_prompt = user_prompt.replace(item["flag"], '')

    result += user_prompt.strip()

    if r'\l' not in args:
        result += f" Answer in less than {config.SOFT_COMPLETION_LIMIT} chars!"
    result = result.replace(r'\l', '')

    return result.strip()


def follow_tail(file_path: str) -> typing.Generator:
    """
    Follows the tail of a file, yielding new lines as they are added.
    """
    first_call = True
    while True:
        try:
            with codecs.open(file_path, encoding='utf-8', errors='ignore') as input:
                if first_call:
                    input.seek(0, 2)
                    first_call = False
                latest_data = input.read()
                while True:
                    if '\n' not in latest_data:
                        latest_data += input.read()
                        if '\n' not in latest_data:
                            yield ''
                            if not os.path.isfile(file_path):
                                break
                            time.sleep(0.1)
                            continue
                    latest_lines = latest_data.split('\n')
                    if latest_data[-1] != '\n':
                        latest_data = latest_lines[-1]
                    else:
                        latest_data = input.read()
                    for line in latest_lines[:-1]:
                        yield line + '\n'
        except Exception as e:
            print(e)
            yield ''


def parse_line(line: str) -> LogLine:
    parts = line.split(" :  ")
    is_team_mes = '(TEAM)' in line
    username = parts[0].replace('(TEAM)', '', 1).removeprefix("*DEAD*").strip()

    if len(parts) > 2:
        prompt = ' '.join(parts[1:])
    else:
        prompt = parts[-1]

    return LogLine(prompt, username, is_team_mes)


def get_console_logline() -> typing.Generator:
    """
    Opens a log file for Team Fortress 2 and yields tuples containing user prompts and usernames.
    """
    for line in follow_tail(config.TF2_LOGFILE_PATH):

        try:
            res = parse_line(line)
        except Exception:
            print("Unknown error happened while reading chat.")
            res = LogLine('', '', False)
        finally:
            yield res
