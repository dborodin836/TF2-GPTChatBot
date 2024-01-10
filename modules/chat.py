from config import config
from modules.api.github import check_for_updates
from modules.bans import is_banned_username, load_banned_players
from modules.bot_state import get_bot_state
from modules.command_controllers import CommandController
from modules.commands.clear_chat import handle_clear
from modules.commands.github import handle_gh_command
from modules.commands.openai import gpt3_handler, h_gpt4, h_gpt4l, handle_cgpt
from modules.commands.rtd import handle_rtd_command
from modules.commands.textgen_webui import handle_custom_chat, handle_custom_model
from modules.logs import get_logger, print_buffered_config_innit_messages
from modules.servers.tf2 import check_connection, get_username
from modules.message_queueing import messaging_queue_service
from modules.utils.prompts import load_prompts
from modules.utils.text import get_console_logline

gui_logger = get_logger("gui")
main_logger = get_logger("main")
combo_logger = get_logger("combo")


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

    controller = CommandController({"CHAT_CONVERSATION_HISTORY": []})

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

    controller.register_service(messaging_queue_service)

    for logline in get_console_logline():
        if not get_bot_state():
            continue
        if is_banned_username(logline.username):
            continue
        controller.process_line(logline)
