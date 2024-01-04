import queue
import threading
import time

from config import config
from services.chatgpt import handle_cgpt_request, handle_gpt_request
from services.github import check_for_updates
from services.source_game import check_connection, get_username, send_say_command_to_tf2
from utils.bans import is_banned_username, load_banned_players
from utils.bot_state import get_bot_state
from utils.commands import handle_custom_model_command, handle_gh_command, handle_rtd_command
from utils.io_buffer import print_buffered_config_innit_messages
from utils.logs import get_logger, log_gui_model_message
from utils.prompt import load_prompts
from utils.text import get_console_logline
from utils.types import LogLine, MessageHistory

PROMPTS_QUEUE: queue.Queue = queue.Queue()

gui_logger = get_logger("gui")
main_logger = get_logger("main")


def set_host_username() -> None:
    """
    Sets the username in config.
    """
    username = get_username()
    config.HOST_USERNAME = username
    gui_logger.info(f"Hello '{config.HOST_USERNAME}'!")


def setup() -> None:
    """
    Initializes the program.
    """
    gui_logger.info(
        r"""
      _____ _____ ____        ____ ____ _____ ____ _           _   ____        _   
     |_   _|  ___|___ \      / ___|  _ \_   _/ ___| |__   __ _| |_| __ )  ___ | |_ 
       | | | |_    __) |____| |  _| |_) || || |   | '_ \ / _` | __|  _ \ / _ \| __|
       | | |  _|  / __/_____| |_| |  __/ | || |___| | | | (_| | |_| |_) | (_) | |_ 
       |_| |_|   |_____|     \____|_|    |_| \____|_| |_|\__,_|\__|____/ \___/ \__|

    """
    )
    check_for_updates()
    check_connection()
    set_host_username()
    load_prompts()
    load_banned_players()
    print_buffered_config_innit_messages()


def parse_console_logs_and_build_conversation_history() -> None:
    """
    Processes the console logs and builds a conversation history, filters banned usernames.
    """
    conversation_history: MessageHistory = []

    setup()

    for logline in get_console_logline():
        if not get_bot_state():
            continue
        if is_banned_username(logline.username):
            continue
        conversation_history = handle_command(logline, conversation_history)


def has_command(prompt: str, command: str) -> bool:
    """
    Check if given command matches with the beginning of the given prompt in a non-case-sensitive manner.
    """
    # TODO: if statements has to be ordered specifically to work properly
    #       ie. !gpt4 -> !gpt4p, !gpt4p will never be triggered
    return prompt.strip().lower().startswith(command.lower())


def handle_command(logline: LogLine, conversation_history: MessageHistory) -> MessageHistory:
    prompt = logline.prompt
    user = logline.username
    is_team = logline.is_team_message

    if has_command(prompt, config.GPT_COMMAND):
        if prompt.removeprefix(config.GPT_COMMAND).strip() == "":
            time.sleep(1)
            send_say_command_to_tf2(
                "Hello there! I am ChatGPT, a ChatGPT plugin integrated into"
                " Team Fortress 2. Ask me anything!",
                team_chat=is_team,
            )
            log_gui_model_message("gpt-3.5-turbo", user, prompt.strip())
            main_logger.info(f"Empty '{config.GPT_COMMAND}' command from user '{user}'.")
            return conversation_history

        main_logger.info(f"'{config.GPT_COMMAND}' command from user '{user}'. "
                         f"Message: '{prompt.removeprefix(config.GPT_COMMAND).strip()}'")
        handle_gpt_request(
            user,
            prompt.removeprefix(config.GPT_COMMAND).strip(),
            model="gpt-3.5-turbo",
            is_team=is_team,
        )

    elif has_command(prompt, config.CHATGPT_COMMAND):
        main_logger.info(f"'{config.CHATGPT_COMMAND}' command from user '{user}'. "
                         f"Message: '{prompt.removeprefix(config.GPT_COMMAND).strip()}'")
        return handle_cgpt_request(
            user,
            prompt.removeprefix(config.CHATGPT_COMMAND).strip(),
            conversation_history,
            is_team=is_team,
            model="gpt-3.5-turbo",
        )

    elif has_command(prompt, "!gpt4l"):
        main_logger.info(f"'!gpt4l' command from user '{user}'. "
                         f"Message: '{prompt.removeprefix(config.GPT_COMMAND).strip()}'")
        if config.GPT4_ADMIN_ONLY and config.HOST_USERNAME == user or not config.GPT4_ADMIN_ONLY:
            return handle_cgpt_request(
                user,
                prompt.removeprefix(config.CHATGPT_COMMAND).strip(),
                conversation_history,
                is_team=is_team,
                model="gpt-4",
            )

    elif has_command(prompt, "!gpt4"):
        main_logger.info(f"'!gpt4' command from user '{user}'. "
                         f"Message: '{prompt.removeprefix(config.GPT_COMMAND).strip()}'")
        if config.GPT4_ADMIN_ONLY and config.HOST_USERNAME == user or not config.GPT4_ADMIN_ONLY:
            return handle_cgpt_request(
                user,
                prompt.removeprefix(config.CHATGPT_COMMAND).strip(),
                conversation_history,
                is_team=is_team,
                model="gpt-4-1106-preview",
            )

    elif has_command(prompt, config.CLEAR_CHAT_COMMAND):
        main_logger.info(f"'{config.CLEAR_CHAT_COMMAND}' command from user '{user}'.")
        log_gui_model_message("CHAT", user, "CLEARING CHAT")
        return []

    elif has_command(prompt, config.RTD_COMMAND):
        main_logger.info(f"'{config.RTD_COMMAND}' command from user '{user}'.")
        handle_rtd_command(user, is_team=is_team)

    elif has_command(prompt, "!gh"):
        main_logger.info(f"'!gh' command from user '{user}'.")
        handle_gh_command(user, is_team=is_team)

    elif has_command(prompt, config.CUSTOM_MODEL_COMMAND):
        main_logger.info(f"'{config.CUSTOM_MODEL_COMMAND}' command from user '{user}'. "
                         f"Message: '{prompt.removeprefix(config.GPT_COMMAND).strip()}'")
        if config.ENABLE_CUSTOM_MODEL:
            if not any([thread.name == "custom" for thread in threading.enumerate()]):
                threading.Thread(
                    target=handle_custom_model_command,
                    args=(user, is_team, prompt),
                    daemon=True,
                    name="custom",
                ).start()

    return conversation_history
