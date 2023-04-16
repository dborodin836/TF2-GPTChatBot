import os
import queue
from io import StringIO

from config import config, output
from services.chatgpt import handle_gpt_request
from services.network import check_connection
from utils.bans import unban_player, ban_player, load_banned_players, is_banned_username
from utils.commands import handle_rtd_command, stop_bot, start_bot, get_bot_state
from utils.prompt import load_prompts
from utils.text import open_tf2_logfile
from utils.logs import log_message

PROMPTS_QUEUE = queue.Queue()


def parse_tf2_console_logs() -> None:
    conversation_history: str = ''

    print("""
  _____ _____ ____        ____ ____ _____ ____ _           _   ____        _   
 |_   _|  ___|___ \      / ___|  _ \_   _/ ___| |__   __ _| |_| __ )  ___ | |_ 
   | | | |_    __) |____| |  _| |_) || || |   | '_ \ / _` | __|  _ \ / _ \| __|
   | | |  _|  / __/_____| |_| |  __/ | || |___| | | | (_| | |_| |_) | (_) | |_ 
   |_| |_|   |_____|     \____|_|    |_| \____|_| |_|\__,_|\__|____/ \___/ \__|
                                                                               
""")

    check_connection()
    load_prompts()
    load_banned_players()

    output.seek(0)

    if get_io_string_size(output) > 0:
        for line in output:
            print(line, end='')
    else:
        print("Ready to use!")

    for line, user in open_tf2_logfile():
        if not get_bot_state():
            continue
        if is_banned_username(user):
            continue
        conversation_history = handle_command(line, user, conversation_history)


def get_io_string_size(string_io: StringIO):
    output.seek(0, os.SEEK_END)
    length = string_io.tell()
    output.seek(0)
    return length


def handle_command(line: str, user: str, conversation_history: str) -> str:
    if line.strip().startswith(config.GPT_COMMAND):
        return handle_gpt_request("GPT3", user, line.removeprefix(config.GPT_COMMAND).strip(),
                                  conversation_history)

    elif line.strip().startswith(config.CHATGPT_COMMAND):
        return handle_gpt_request("CHAT", user, line.removeprefix(config.CHATGPT_COMMAND).strip(),
                                  conversation_history)

    elif line.strip().startswith(config.CLEAR_CHAT_COMMAND):
        log_message("CHAT", user, "CLEARING CHAT")
        return ''

    elif line.strip().startswith("!rtd"):
        handle_rtd_command(user)

    elif line.strip() == "!gpt_stop":
        stop_bot()

    elif line.strip() == "!gpt_start":
        start_bot()

    elif line.strip().startswith("ban "):
        name = line.removeprefix("ban ").strip()
        ban_player(name)

    elif line.strip().startswith("unban "):
        name = line.removeprefix("unban ").strip()
        unban_player(name)
    return conversation_history
