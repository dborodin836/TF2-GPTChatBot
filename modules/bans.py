import codecs
import json
from json import JSONDecodeError

from modules.logs import get_logger, log_gui_general_message

main_logger = get_logger("main")
gui_logger = get_logger("gui")
combo_logger = get_logger("combo")

BANNED_PLAYERS = set()
BANS_FILE = "bans.json"


def load_banned_players() -> set:
    """
    Loads the set of banned players.
    """
    try:
        with codecs.open(BANS_FILE, "r", encoding="utf-8") as f:
            banned_players = set(json.load(f))
    except (EOFError, JSONDecodeError):
        banned_players = set()
    except FileNotFoundError:
        combo_logger.warning(f"File {BANS_FILE} could not be found.")
        banned_players = set()
    except Exception as e:
        combo_logger.warning(f"Failed to load banned players. [{e}]")
        banned_players = set()

    return banned_players


def is_banned_username(username: str) -> bool:
    """
    Checks if a given username is banned.
    """
    main_logger.trace(f"Checking if '{username}' is banned.")
    return username in BANNED_PLAYERS


def unban_player(username: str) -> None:
    """
    Removes a player from the set of banned players.
    """
    main_logger.debug(f"Trying to unban '{username}'")
    if is_banned_username(username):
        BANNED_PLAYERS.remove(username)
        log_gui_general_message(f"UNBANNED '{username}'")
        main_logger.debug(f"Successfully unbanned {username}")
        with codecs.open(BANS_FILE, "w", encoding="utf-8") as f:
            json.dump(list(BANNED_PLAYERS), f)
    else:
        log_gui_general_message(f"USER '{username}' WAS NOT BANNED!")
        main_logger.debug(f"{username} was not banned, cancelling.")


def get_banned_players() -> set:
    return BANNED_PLAYERS


def ban_player(username: str) -> None:
    """
    Adds a player to the set of banned players.
    """
    main_logger.debug(f"Trying to ban '{username}'")
    if not is_banned_username(username):
        BANNED_PLAYERS.add(username)
        log_gui_general_message(f"BANNED '{username}'")
        main_logger.debug(f"Successfully banned {username}")
        with codecs.open(BANS_FILE, "w", encoding="utf-8") as f:
            json.dump(list(BANNED_PLAYERS), f)
    else:
        log_gui_general_message(f"'{username}' ALREADY BANNED")
        main_logger.debug(f"{username} already banned.")


def list_banned_players() -> None:
    """
    Prints a list of currently banned players.
    """
    if len(BANNED_PLAYERS) == 0:
        gui_logger.info("### NO BANS ###")
    else:
        gui_logger.info("### BANNED PLAYERS ###")
        for user in list(BANNED_PLAYERS):
            gui_logger.info(f"- {user}")
