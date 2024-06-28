from modules.bans import bans_manager
from modules.command_controllers import InitializerConfig
from modules.lobby_manager import lobby_manager
from modules.logs import gui_logger


def handle_ban(command: str, shared_dict: InitializerConfig):
    username = command.removeprefix("ban ").strip()
    player = lobby_manager.get_player_by_name(username)
    if player is not None:
        bans_manager.ban_player(player)
        return None
    gui_logger.info(f"Player '{username}' not found.")


def handle_unban(command: str, shared_dict: InitializerConfig):
    username = command.removeprefix("unban ").strip()
    player = lobby_manager.get_player_by_name(username)
    if player is not None:
        bans_manager.unban_player(player)
        return None
    gui_logger.info(f"Player '{username}' not found.")


def handle_list_bans(command: str, shared_dict: InitializerConfig):
    if len(bans_manager.banned_players_steamid3) == 0:
        gui_logger.info("### NO BANS ###")
    else:
        gui_logger.info(
            "### BANNED PLAYERS ###", *list(bans_manager.banned_players_steamid3), sep="\n"
        )
