from config import config
from modules.api.github import check_for_updates
from modules.bans import bans_manager
from modules.bot_state import state_manager
from modules.command_controllers import CommandController, InitializerConfig
from modules.commands.clear_chat import handle_clear
from modules.commands.github import handle_gh_command
from modules.commands.groq import GroqQuickQueryCommand, GroqGlobalChatCommand, GroqPrivateChatCommand
from modules.commands.openai import OpenAIGlobalChatCommand, OpenAIPrivateChatCommand, OpenAIGPT3QuickQueryCommand, \
    OpenAIGPT4QuickQueryCommand, OpenAIGPT4LQuickQueryCommand
from modules.commands.rtd import handle_rtd
from modules.commands.textgen_webui import TextgenWebUIGlobalChatCommand, TextgenWebUIPrivateChatCommand, \
    TextgenWebUIQuickQueryCommand
from modules.logs import get_logger
from modules.message_queueing import messaging_queue_service
from modules.servers.tf2 import check_connection, set_host_username
from modules.utils.buffered_messages import print_buffered_config_innit_messages
from modules.utils.prompts import load_prompts
from modules.utils.steam import set_host_steamid3
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
    set_host_steamid3()
    load_prompts()
    print_buffered_config_innit_messages()


def parse_console_logs_and_build_conversation_history() -> None:
    """
    Processes the console logs and builds a conversation history, filters banned usernames.
    """
    setup()

    controller = CommandController(InitializerConfig())

    # Commands
    controller.register_command("!gh", handle_gh_command)
    controller.register_command(config.RTD_COMMAND, handle_rtd)
    controller.register_command(config.CLEAR_CHAT_COMMAND, handle_clear)
    if config.ENABLE_OPENAI_COMMANDS:
        controller.register_command(config.GPT4_COMMAND, OpenAIGPT4QuickQueryCommand.as_command())
        controller.register_command(config.GPT4_LEGACY_COMMAND, OpenAIGPT4LQuickQueryCommand.as_command())
        controller.register_command(config.CHATGPT_COMMAND, OpenAIPrivateChatCommand.as_command())
        controller.register_command(config.GLOBAL_CHAT_COMMAND, OpenAIGlobalChatCommand.as_command())
        controller.register_command(config.GPT_COMMAND, OpenAIGPT3QuickQueryCommand.as_command())
    if config.ENABLE_CUSTOM_MODEL:
        controller.register_command(config.CUSTOM_MODEL_COMMAND, TextgenWebUIQuickQueryCommand.as_command())
        controller.register_command(config.CUSTOM_MODEL_CHAT_COMMAND, TextgenWebUIPrivateChatCommand.as_command())
        controller.register_command(config.GLOBAL_CUSTOM_CHAT_COMMAND, TextgenWebUIGlobalChatCommand.as_command())
    if config.GROQ_ENABLE:
        controller.register_command(config.GROQ_COMMAND, GroqQuickQueryCommand.as_command())
        controller.register_command(config.GROQ_CHAT_COMMAND, GroqGlobalChatCommand.as_command())
        controller.register_command(config.GROQ_PRIVATE_CHAT, GroqPrivateChatCommand.as_command())

    # Services
    controller.register_service(messaging_queue_service)

    for logline in get_console_logline():
        if logline is None:
            continue
        if not state_manager.bot_running:
            continue
        if bans_manager.is_banned_player(logline.player):
            main_logger.info(f"Player '{logline.player.name}' {logline.player.steamid3} tried to use commands, but "
                             f"he's banned.")
            continue
        controller.process_line(logline)
