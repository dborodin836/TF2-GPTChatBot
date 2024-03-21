import codecs
import json
from json import JSONDecodeError
from typing import Set

from modules.logs import get_logger, log_gui_general_message
from modules.typing import Player

main_logger = get_logger("main")
gui_logger = get_logger("gui")
combo_logger = get_logger("combo")


class BansManager:
    def __init__(self, bans_file: str = None):
        self.banned_players_steamid3: Set[str] = set()
        self.__bans_filename = bans_file or "bans.json"
        self.load_banned_players()

    def load_banned_players(self) -> None:
        """
        Loads the set of banned players.
        """
        try:
            with codecs.open(self.__bans_filename, "r", encoding="utf-8") as file:
                self.banned_players_steamid3 = set(json.load(file))
        except (EOFError, JSONDecodeError) as e:
            combo_logger.warning(f"Error parsing .json file [{e}].")
            self.banned_players_steamid3 = set()
        except FileNotFoundError:
            combo_logger.warning(f"File {self.__bans_filename} could not be found.")
            self.banned_players_steamid3 = set()
        except Exception as e:
            combo_logger.warning(f"Failed to load banned players. [{e}]")
            self.banned_players_steamid3 = set()

    def is_banned_player(self, player: Player) -> bool:
        """
        Checks if a given username is banned.
        """
        main_logger.trace(f"Checking if '{player.name}' [{player.steamid64}] is banned.")
        return player.steamid3 in self.banned_players_steamid3

    def ban_player(self, player: Player) -> None:
        """
        Adds a player to the set of banned players.
        """
        main_logger.debug(f"Trying to ban '{player.name}' [{player.steamid64}]")
        if not self.is_banned_player(player):
            self.banned_players_steamid3.add(player.steamid3)
            log_gui_general_message(f"BANNED '{player}' [{player.steamid64}]")
            main_logger.debug(f"Successfully banned {player} [{player.steamid64}]")
            with codecs.open(self.__bans_filename, "w", encoding="utf-8") as f:
                json.dump(list(self.banned_players_steamid3), f)
        else:
            log_gui_general_message(f"='{player}' [{player.steamid64}] ALREADY BANNED")
            main_logger.debug(f"{player} [{player.steamid64}] already banned.")

    def unban_player(self, player: Player) -> None:
        """
        Removes a player from the set of banned players.
        """
        main_logger.debug(f"Trying to unban '{player}' [{player.steamid64}]")
        if self.is_banned_player(player):
            self.banned_players_steamid3.remove(player.steamid3)
            log_gui_general_message(f"UNBANNED '{player}' [{player.steamid64}]")
            main_logger.debug(f"Successfully unbanned {player} [{player.steamid64}]")
            with codecs.open(self.__bans_filename, "w", encoding="utf-8") as f:
                json.dump(list(self.banned_players_steamid3), f)
        else:
            log_gui_general_message(f"USER '{player}' WAS NOT BANNED!")
            main_logger.debug(f"{player} [{player.steamid64}] was not banned, cancelling.")


bans_manager = BansManager()
