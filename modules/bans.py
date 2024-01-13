import codecs
import json
from json import JSONDecodeError

from modules.logs import get_logger, log_gui_general_message

main_logger = get_logger("main")
gui_logger = get_logger("gui")
combo_logger = get_logger("combo")


class BansManager:
    def __init__(self, bans_file: str = None):
        self.banned_usernames = set()
        self.__bans_filename = bans_file or "bans.json"
        self.load_banned_players()

    def load_banned_players(self):
        """
            Loads the set of banned players.
        """
        try:
            with codecs.open(self.__bans_filename, "r", encoding="utf-8") as file:
                self.banned_usernames = set(json.load(file))
        except (EOFError, JSONDecodeError):
            self.banned_usernames = set()
        except FileNotFoundError:
            combo_logger.warning(f"File {self.__bans_filename} could not be found.")
            self.banned_usernames = set()
        except Exception as e:
            combo_logger.warning(f"Failed to load banned players. [{e}]")
            self.banned_usernames = set()

    def is_banned_username(self, username: str) -> bool:
        """
        Checks if a given username is banned.
        """
        main_logger.trace(f"Checking if '{username}' is banned.")
        return username in self.banned_usernames

    def ban_player(self, username: str) -> None:
        """
        Adds a player to the set of banned players.
        """
        main_logger.debug(f"Trying to ban '{username}'")
        if not self.is_banned_username(username):
            self.banned_usernames.add(username)
            log_gui_general_message(f"BANNED '{username}'")
            main_logger.debug(f"Successfully banned {username}")
            with codecs.open(self.__bans_filename, "w", encoding="utf-8") as f:
                json.dump(list(self.banned_usernames), f)
        else:
            log_gui_general_message(f"='{username}' ALREADY BANNED")
            main_logger.debug(f"{username} already banned.")

    def unban_player(self, username: str) -> None:
        """
        Removes a player from the set of banned players.
        """
        main_logger.debug(f"Trying to unban '{username}'")
        if self.is_banned_username(username):
            self.banned_usernames.remove(username)
            log_gui_general_message(f"UNBANNED '{username}'")
            main_logger.debug(f"Successfully unbanned {username}")
            with codecs.open(self.__bans_filename, "w", encoding="utf-8") as f:
                json.dump(list(self.banned_usernames), f)
        else:
            log_gui_general_message(f"USER '{username}' WAS NOT BANNED!")
            main_logger.debug(f"{username} was not banned, cancelling.")


bans_manager = BansManager()
