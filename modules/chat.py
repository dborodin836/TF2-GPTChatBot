from config import config
from modules.api.github import check_for_updates
from modules.bans import bans_manager
from modules.bot_state import state_manager
from modules.command_controllers import CommandController
from modules.commands.clear_chat import handle_clear
from modules.commands.github import handle_gh_command
from modules.commands.openai import handle_gpt3, handle_gpt4, handle_gpt4l, handle_cgpt
from modules.commands.rtd import handle_rtd
from modules.commands.textgen_webui import handle_custom_chat, handle_custom_model
from modules.logs import get_logger
from modules.utils.buffered_messages import print_buffered_config_innit_messages
from modules.servers.tf2 import check_connection, set_host_username
from modules.message_queueing import messaging_queue_service
from modules.utils.prompts import load_prompts
from modules.utils.text import get_console_logline

gui_logger = get_logger("gui")
main_logger = get_logger("main")
combo_logger = get_logger("combo")


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
    print_buffered_config_innit_messages()


def parse_console_logs_and_build_conversation_history() -> None:
    """
    Processes the console logs and builds a conversation history, filters banned usernames.
    """
    setup()

    controller = CommandController({"CHAT_CONVERSATION_HISTORY": []})

    controller.register_command("!gh", handle_gh_command)
    controller.register_command("!gpt4", handle_gpt4)
    controller.register_command("!gpt4l", handle_gpt4l)
    controller.register_command(config.RTD_COMMAND, handle_rtd)
    controller.register_command(config.GPT_COMMAND, handle_gpt3)
    controller.register_command(config.CHATGPT_COMMAND, handle_cgpt)
    controller.register_command(config.CLEAR_CHAT_COMMAND, handle_clear)
    controller.register_command(config.CUSTOM_MODEL_COMMAND, handle_custom_model)
    controller.register_command(config.CUSTOM_MODEL_CHAT_COMMAND, handle_custom_chat)

    controller.register_service(messaging_queue_service)

    for logline in get_console_logline():
        if not state_manager.bot_running:
            continue
        if bans_manager.is_banned_username(logline.username):
            continue
        controller.process_line(logline)
