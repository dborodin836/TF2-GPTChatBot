import difflib
import time
from statistics import mean
from typing import Any, List, Optional

from modules.typing import Player
from modules.logs import get_logger
from modules.utils.steam import steamid3_to_steamid64

main_logger = get_logger("combo")


def find_username(username: str, data: List) -> Optional[str] | Any:
    if len(data) == 0:
        return None
    matches = []

    for candidate in data:
        if candidate in username:
            matches.append(candidate)

    if len(matches) == 1:
        return matches[0]

    diff = difflib.get_close_matches(username, matches, n=1, cutoff=0.8)
    if len(diff) == 0:
        return None
    if type(diff) is str:
        return diff
    elif type(diff) is list:
        return diff[0]


class LobbyManager:
    def __init__(self):
        self.players: List[Player] = list()

    def get_player_by_name(self, username: str) -> Optional[Player]:
        for plr in self.players:
            if plr.name == username:
                return plr
        return None

    def search_username(self, username: str) -> str:
        data = [plr.name for plr in self.players]
        usr = find_username(username, data)
        if usr is not None:
            return usr
        return username

    def is_username_exist(self, username: str) -> bool:
        for player in self.players:
            if username == player.name:
                return True

        return False

    def add_player(self, new_player: Player) -> None:
        for player in self.players:
            # If player already exist
            if player.name == new_player.name:
                # Update minutes on server and last_updated
                player.minutes_on_server = new_player.minutes_on_server
                player.last_updated = time.time()

                # Update ping
                player.ping_list.append(new_player.ping)
                player.ping = round(mean(player.ping_list))

                main_logger.trace(f"Updated players time on server {player.name}")
                return

        # New player
        new_player.steamid64 = steamid3_to_steamid64(new_player.steamid3)
        self.players.append(new_player)
        main_logger.debug(
            f"Added new player {new_player.name} with {new_player.minutes_on_server} minutes on server"
        )


lobby_manager = LobbyManager()
