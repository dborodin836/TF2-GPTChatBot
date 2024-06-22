from config import RTDModes, config
from modules.api.github import check_for_updates
from modules.bans import bans_manager
from modules.bot_state import state_manager
from modules.builder.utils import load_commands
from modules.command_controllers import CommandController, InitializerConfig
from modules.commands.clear_chat import handle_clear
from modules.commands.github import handle_gh_command
from modules.commands.rtd import handle_rtd
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

controller = CommandController(InitializerConfig())


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
    load_commands(controller)
    load_prompts()
    check_connection()
    set_host_username()
    set_host_steamid3()
    print_buffered_config_innit_messages()


def parse_console_logs_and_build_conversation_history() -> None:
    """
    Processes the console logs and builds a conversation history, filters banned usernames.
    """
    setup()

    # Commands
    controller.register_command("!gh", handle_gh_command)
    controller.register_command(config.CLEAR_CHAT_COMMAND, handle_clear)
    if config.RTD_MODE != RTDModes.DISABLED:
        controller.register_command(config.RTD_COMMAND, handle_rtd, "rtd")

    # Services
    controller.register_service(messaging_queue_service)

    for logline in get_console_logline():
        if logline is None:
            continue
        if not state_manager.bot_running:
            continue
        if bans_manager.is_banned_player(logline.player):
            main_logger.info(
                f"Player '{logline.player.name}' {logline.player.steamid3} tried to use commands, but "
                f"he's banned."
            )
            continue
        controller.process_line(logline)
