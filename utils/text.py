import codecs
import re
import time
import os
from typing import Tuple

from config import TF2_LOGFILE_PATH, SOFT_COMPLETION_LIMIT
from utils.prompt import PROMPTS

MAX_LENGTH_CYRILLIC = 65
MAX_LENGTH_OTHER = 120


def follow(logfile) -> Tuple[str, str]:
    """
    Continuously monitoring a log file
    """
    logfile.seek(0, os.SEEK_END)  # Go to the end of the file

    while True:
        try:
            line = logfile.readline()
        except Exception:
            continue

        if not line:
            time.sleep(0.1)
            continue
        #  This yields a tuple containing the user prompt and the username.
        #  ('!gpt3 Who are you Chatgpt?', 'username')
        yield line.split(" :  ")[-1], line.split(" :  ")[0]


def get_chunks(s, maxlength):
    """
    This function splits a string into chunks of a maximum length, with each chunk ending at the
    last space character before the maximum length.
    """
    start = 0
    end = 0
    while start + maxlength < len(s) and end != -1:
        end = s.rfind(" ", start, start + maxlength + 1)
        yield s[start:end]
        start = end + 1
    yield s[start:]


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
    #  This args var also contains user prompt lul
    args = user_prompt.split(' ')
    result = ''

    for item in PROMPTS:
        if item["flag"] in args:
            result += item["prompt"]
            user_prompt = user_prompt.replace(item["flag"], '')

    result += user_prompt.strip()

    if r'\l' not in args:
        result += f" Answer in less than {SOFT_COMPLETION_LIMIT} chars!"
    result = result.replace(r'\l', '')

    return result


def open_tf2_logfile() -> Tuple[str, str]:
    logfile = codecs.open(TF2_LOGFILE_PATH, "r", encoding='utf-8')
    return follow(logfile)
