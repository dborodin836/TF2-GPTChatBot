import codecs
import json
from json import JSONDecodeError

from utils.logs import log_cmd_message

BANNED_PLAYERS = set()
BANS_FILE = 'bans.json'


async def load_banned_players() -> set:
    """
    Loads the set of banned players.
    """
    try:
        with codecs.open(BANS_FILE, 'r', encoding='utf-8') as f:
            banned_players = set(json.load(f))
    except (EOFError, JSONDecodeError):
        banned_players = set()
    except FileNotFoundError:
        banned_players = set()
        print(f'File {BANS_FILE} could not be found.')

    print(f"Loaded {len(banned_players)} player bans.")
    return banned_players


def is_banned_username(username: str) -> bool:
    """
    Checks if a given username is banned.
    """
    return username in BANNED_PLAYERS


def unban_player(username: str) -> None:
    """
    Removes a player from the set of banned players.
    """
    if is_banned_username(username):
        BANNED_PLAYERS.remove(username)
        log_cmd_message(f"UNBANNED '{username}'")
        with codecs.open(BANS_FILE, 'w', encoding='utf-8') as f:
            json.dump(list(BANNED_PLAYERS), f)
    else:
        log_cmd_message(f"USER '{username}' WAS NOT BANNED!")


def ban_player(username: str) -> None:
    """
    Adds a player to the set of banned players.
    """
    if not is_banned_username(username):
        BANNED_PLAYERS.add(username)
        log_cmd_message(f"BANNED '{username}'")
        with codecs.open(BANS_FILE, 'w', encoding='utf-8') as f:
            json.dump(list(BANNED_PLAYERS), f)
    else:
        log_cmd_message(f"USER '{username}' ALREADY BANNED")


def list_banned_players() -> None:
    """
    Prints a list of currently banned players.
    """
    if len(BANNED_PLAYERS) == 0:
        print("### NO BANS ###")
    else:
        print("### BANNED PLAYERS ###", *list(BANNED_PLAYERS), sep='\n')
