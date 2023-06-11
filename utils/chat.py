import queue
import time

from config import config
from services.chatgpt import handle_cgpt_request, handle_gpt_request
from services.github import check_for_updates
from services.source_game import check_connection, send_say_command_to_tf2, get_username
from utils.bans import unban_player, ban_player, load_banned_players, is_banned_username
from utils.commands import handle_rtd_command, handle_gh_command
from utils.bot_state import start_bot, stop_bot, get_bot_state
from utils.prompt import load_prompts
from utils.text import get_console_logline
from utils.types import LogLine
from utils.logs import log_message
from utils.types import MessageHistory
from utils.io_buffer import print_buffered_config_innit_messages

PROMPTS_QUEUE: queue.Queue = queue.Queue()


def set_host_username() -> None:
    """
    Sets the username in config.
    """
    username = get_username()
    config.HOST_USERNAME = username
    print(f"Hello '{config.HOST_USERNAME}'!")


def setup() -> None:
    """
    Initializes the program.
    """
    print(r"""
      _____ _____ ____        ____ ____ _____ ____ _           _   ____        _   
     |_   _|  ___|___ \      / ___|  _ \_   _/ ___| |__   __ _| |_| __ )  ___ | |_ 
       | | | |_    __) |____| |  _| |_) || || |   | '_ \ / _` | __|  _ \ / _ \| __|
       | | |  _|  / __/_____| |_| |  __/ | || |___| | | | (_| | |_| |_) | (_) | |_ 
       |_| |_|   |_____|     \____|_|    |_| \____|_| |_|\__,_|\__|____/ \___/ \__|

    """)

    check_for_updates()
    check_connection()
    set_host_username()
    load_prompts()
    load_banned_players()
    print_buffered_config_innit_messages()


def parse_console_logs_and_build_conversation_history() -> None:
    conversation_history: MessageHistory = []

    setup()

    for logline in get_console_logline():
        if not get_bot_state():
            continue
        if is_banned_username(logline.username):
            continue
        conversation_history = handle_command(logline, conversation_history)


def has_command(prompt: str, command: str) -> bool:
    return prompt.strip().lower().startswith(command.lower())


def handle_command(logline: LogLine, conversation_history: MessageHistory) -> MessageHistory:
    prompt = logline.prompt
    user = logline.username
    is_team = logline.is_team_message

    if has_command(prompt, config.GPT_COMMAND):
        if prompt.removeprefix(config.GPT_COMMAND).strip() == "":
            time.sleep(1)
            send_say_command_to_tf2("Hello there! I am ChatGPT, a ChatGPT plugin integrated into"
                                    " Team Fortress 2. Ask me anything!", team_chat=is_team)
            log_message('GPT3', user, prompt.strip())
            return conversation_history

        handle_gpt_request(user, prompt.removeprefix(config.GPT_COMMAND).strip(),
                           is_team=is_team)

    elif has_command(prompt, config.CHATGPT_COMMAND):
        return handle_cgpt_request(user, prompt.removeprefix(config.CHATGPT_COMMAND).strip(),
                                   conversation_history, is_team=is_team)

    elif has_command(prompt, config.CLEAR_CHAT_COMMAND):
        log_message("CHAT", user, "CLEARING CHAT")
        return []

    elif has_command(prompt, config.RTD_COMMAND):
        handle_rtd_command(user, is_team=is_team)

    elif has_command(prompt, '!gh'):
        handle_gh_command(user, is_team=is_team)

    # console echo commands start
    elif prompt.strip() == "!gpt_stop":
        stop_bot()

    elif prompt.strip() == "!gpt_start":
        start_bot()

    elif prompt.strip().startswith("ban "):
        name = prompt.removeprefix("ban ").strip()
        ban_player(name)

    elif prompt.strip().startswith("unban "):
        name = prompt.removeprefix("unban ").strip()
        unban_player(name)
    # console echo commands end

    return conversation_history
