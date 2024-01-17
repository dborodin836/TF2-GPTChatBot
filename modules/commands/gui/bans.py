from modules.bans import bans_manager
from modules.logs import get_logger

gui_logger = get_logger("gui")


def handle_ban(command, shared_dict):
    username = command.removeprefix("ban ").strip()
    bans_manager.ban_player(username)


def handle_unban(command, shared_dict):
    name = command.removeprefix("unban ").strip()
    bans_manager.unban_player(name)


def handle_list_bans(command, shared_dict):
    if len(bans_manager.banned_usernames) == 0:
        gui_logger.info("### NO BANS ###")
    else:
        gui_logger.info("### BANNED PLAYERS ###", *list(bans_manager.banned_usernames), sep="\n")
