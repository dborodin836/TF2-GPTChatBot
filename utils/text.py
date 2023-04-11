import codecs
import re
import time
import os
import time
from typing import Tuple

from config import TF2_LOGFILE_PATH, SOFT_COMPLETION_LIMIT
from utils.prompt import PROMPTS

MAX_LENGTH_CYRILLIC = 65
MAX_LENGTH_OTHER = 120


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


def follow_tail(file_path: str) -> str:
    first_call = True
    while True:
        try:
            with codecs.open(file_path, encoding='utf-8') as input:
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
        except IOError:
            yield ''


def open_tf2_logfile() -> Tuple[str, str]:
    for line in follow_tail(TF2_LOGFILE_PATH):
        #  This yields a tuple containing the user prompt and the username.
        #  ('!gpt3 Who are you Chatgpt?', 'username')
        yield line.split(" :  ")[-1], line.split(" :  ")[0].removeprefix("*DEAD* ")
