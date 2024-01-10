from modules.bans import ban_player, unban_player, list_banned_players


def handle_ban(command, shared_dict):
    name = command.removeprefix("ban ").strip()
    ban_player(name)


def handle_unban(command, shared_dict):
    name = command.removeprefix("unban ").strip()
    unban_player(name)


def handle_list_bans(command, shared_dict):
    list_banned_players()
