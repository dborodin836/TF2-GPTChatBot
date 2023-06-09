import codecs
import re
import os
import time
import typing

from config import config
from utils.prompt import PROMPTS
from utils.tf_statistics import StatsData
from utils.types import LogLine, Player

MAX_LENGTH_CYRILLIC = 65
MAX_LENGTH_OTHER = 120

TF2BD_WRAPPER_CHARS = ['\u200e', '\u200d', '\ufeff', '\u200b', '\u200f', '\u202c', '\u2060', '\u200c']
try:
    TF2BD_WRAPPER_FOLDER_EXIST = os.path.exists(os.path.join(
        os.path.dirname(config.TF2_LOGFILE_PATH),
        'custom/aaaaaaaaaa_loadfirst_tf2_bot_detector')
    )
except AttributeError:
    # Nothing bad will happen if we set this to True
    TF2BD_WRAPPER_FOLDER_EXIST = True


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

    if r'\stats' in args and config.ENABLE_STATS:
        result = f" {StatsData.get_data()} Based on this data answer following question. " + result + " Ignore unknown data."
        result = result.replace(r'\stats', '')

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
    if TF2BD_WRAPPER_FOLDER_EXIST:
        for char in TF2BD_WRAPPER_CHARS:
            line = line.replace(char, '')

    parts = line.split(" :  ")
    is_team_mes = '(TEAM)' in line
    username = parts[0].replace('(TEAM)', '', 1).removeprefix("*DEAD*").strip()

    if len(parts) > 2:
        prompt = ' '.join(parts[1:])
    else:
        prompt = parts[-1]

    return LogLine(prompt, username, is_team_mes)


def get_minutes_from_str(time_str: str) -> int:
    try:
        struct_time = time.strptime(time_str, "%H:%M:%S")
        tm = struct_time.tm_hour * 60 + struct_time.tm_min
    except ValueError:
        struct_time = time.strptime(time_str, "%M:%S")
        tm = struct_time.tm_min
    except Exception as e:
        print(f"Unhandled error while parsing time happened. ({e})")
        tm = 0

    return tm


def stats_regexes(line: str):
    # Parsing user line from status command
    if matches := re.search(r"^#\s*\d*\s*\"(.*)\"\s*(\[.*])\s*(\d*:?\d*:\d*)\s*(\d*)\s*\d*\s*\w*\s*\w*", line):
        time_on_server = matches.groups()[2]

        tm = get_minutes_from_str(time_on_server)

        d = Player(
            name=matches.groups()[0],
            minutes_on_server=tm,
            last_updated=tm,
            steamid3=matches.groups()[1],
            ping=matches.groups()[3]
        )

        StatsData.add_player(d)

    # Parsing map name on connection
    elif matches := re.search(r"^Map:\s(\w*)", line):
        map_ = matches.groups()[0]
        StatsData.set_map_name(map_)

    # Parsing server ip
    elif matches := re.search(r"^udp/ip\s*:\s*((\d*.){4}:\d*)", line):
        ip = matches.groups()[0]
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
        except Exception:
            print("Unknown error happened while reading chat.")
            res = LogLine('', '', False)
        finally:
            yield res
