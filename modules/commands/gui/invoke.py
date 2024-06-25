from config import config
from modules.setup import controller
from modules.lobby_manager import lobby_manager
from modules.logs import get_logger
from modules.typing import LogLine

gui_logger = get_logger("main")


def invoke(command, shared_dict):
    prompt = command.removeprefix("@").strip()
    player_lst = list(
        filter(lambda plr: plr.steamid3 == config.HOST_STEAMID3, lobby_manager.players)
    )
    if len(player_lst) != 0:
        player = player_lst[0]
        logline = LogLine(prompt=prompt, is_team_message=False, username=player.name, player=player)
        gui_logger.warning(logline)
        controller.process_line(logline)
