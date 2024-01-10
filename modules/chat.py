import queue
from typing import Optional, Callable

from ordered_set import OrderedSet

from modules.commands.common import handle_clear
from modules.commands.openai import gpt3_handler, handle_cgpt, h_gpt4, h_gpt4l
from modules.commands.textgen_webui import handle_custom_model, handle_custom_chat
from config import config
from modules.services.github import check_for_updates
from modules.services.source_game import check_connection, get_username, q_manager
from modules.bans import is_banned_username, load_banned_players
from modules.bot_state import get_bot_state
from modules.commands.rtd import handle_rtd_command
from modules.commands.github import handle_gh_command
from modules.logs import get_logger, get_time_stamp, print_buffered_config_innit_messages
from modules.prompt import load_prompts
from modules.text import get_console_logline
from modules.types import LogLine

PROMPTS_QUEUE: queue.Queue = queue.Queue()

gui_logger = get_logger("gui")
main_logger = get_logger("main")
combo_logger = get_logger("combo")


class ModificationOfSetKey(Exception):
    pass


class DeletionOfSetKey(Exception):
    pass


class SetOnceDictionary(dict):
    def __setitem__(self, key, value):
        if self.get(key, None) is not None:
            raise ModificationOfSetKey("You cannot modify value after setting it.")
        super().__setitem__(key, value)

    def __delitem__(self, key):
        raise DeletionOfSetKey("You cannot delete value after setting it.")


class CommandController:

    def __init__(self, initializer_config: dict = None) -> None:
        self.__tasks = OrderedSet()
        self.__named_commands_registry: SetOnceDictionary[str, Callable] = SetOnceDictionary()
        self.__shared = dict()

        if initializer_config is not None:
            self.__shared.update(initializer_config)

    def register_command(self, name: str, function: Callable) -> None:
        self.__named_commands_registry[name] = function

    def register_task(self, function: Callable):
        self.__tasks.add(function)

    def process_line(self, logline: LogLine):
        for task in self.__tasks:
            task(logline)

        command_name = logline.prompt.strip().split(" ")[0].lower()

        handler: Optional[Callable] = self.__named_commands_registry.get(command_name, None)
        if handler is None:
            return

        combo_logger.info(f"[{get_time_stamp()}] -- '{command_name}' command from user '{logline.username}'.")
        handler(logline, self.__shared)


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
    setup()

    controller = CommandController({
        "CHAT_CONVERSATION_HISTORY": []
    })

    # TODO: Check what does logline contains, it may contain !gh or smth
    # Or its in some command handlers
    controller.register_command("!gh", handle_gh_command)
    controller.register_command("!gpt4", h_gpt4)
    controller.register_command("!gpt4l", h_gpt4l)
    controller.register_command(config.RTD_COMMAND, handle_rtd_command)
    controller.register_command(config.GPT_COMMAND, gpt3_handler)
    controller.register_command(config.CHATGPT_COMMAND, handle_cgpt)
    controller.register_command(config.CLEAR_CHAT_COMMAND, handle_clear)
    controller.register_command(config.CUSTOM_MODEL_COMMAND, handle_custom_model)
    controller.register_command(config.CUSTOM_MODEL_CHAT_COMMAND, handle_custom_chat)

    for logline in get_console_logline():
        if not get_bot_state():
            continue
        if is_banned_username(logline.username):
            continue
        controller.process_line(logline)


def unlock_q_task(logline: LogLine, **kwargs):
    awaited_msg = q_manager.get_awaited_msg()
    if awaited_msg is not None and awaited_msg in logline.prompt and logline.username == config.HOST_USERNAME:
        q_manager.unlock_queue()
