import re
import sys
import time
from typing import Optional

from rcon import WrongPassword

from config import config
from modules.logs import get_logger
from modules.message_queueing import message_queue
from modules.rcon_client import RconClient
from modules.typing import QueuedMessage
from modules.utils.text import get_chunks, get_shortened_username

main_logger = get_logger("main")
gui_logger = get_logger("gui")
combo_logger = get_logger("combo")


def get_username() -> str:
    try:
        with RconClient() as client:
            response = client.run("name")
    except Exception as e:
        combo_logger.error(f"Failed to get username. [{e}]")

    pattern = r'"name"\s*=\s"(.+?)"'
    match = re.search(pattern, response)

    if match:
        name = match.group(1)
        main_logger.info(f"Found username '{name}'")
        return name
    return ""


def check_connection():
    """
    Continuously tries to log in to a remote RCON server using the provided credentials until a
    successful connection is established. If a connection is refused, the function will wait for
    4 seconds and then try again.
    """
    connected = False
    while not connected:
        main_logger.debug(f"Trying to connect to '{config.RCON_HOST}:{config.RCON_PORT}'")

        try:
            with RconClient() as client:
                connected = client.login(passwd=config.RCON_PASSWORD)
        except WrongPassword:
            combo_logger.critical("Passwords do not match!")
            time.sleep(4)
            sys.exit(1)
        except ConnectionRefusedError:
            combo_logger.warning("Couldn't connect! Retrying in 4 second...")
            time.sleep(4)
        except Exception as e:
            combo_logger.error(f"Unhandled exception happened. [{e}]")
            time.sleep(8)
    combo_logger.info("Successfully connected!")


def format_say_message(message: str, username: Optional[str] = None) -> str:
    # Append username to the first chunk
    if username is not None and config.ENABLE_SHORTENED_USERNAMES_RESPONSE:
        message = f"{get_shortened_username(username)}{message}"

    # No " should be in answer it causes say command to broke
    message = message.replace('"', "")

    return message


def send_say_command_to_tf2(
    message: str, username: Optional[str] = None, is_team_chat: bool = False
) -> None:
    """
    Sends a "say" command to a Team Fortress 2 server using RCON protocol.
    """
    message = format_say_message(message, username)

    msg_chunks = get_chunks(message)

    for msg_chunk in msg_chunks:
        main_logger.trace(f'Adding message "{msg_chunk}" to queue.')
        queued_message = QueuedMessage(text=msg_chunk, is_team_chat=is_team_chat)
        message_queue.put(queued_message)


def set_host_username() -> None:
    """
    Sets the username in config.
    """
    username = get_username()
    config.HOST_USERNAME = username
    gui_logger.info(f"Hello '{config.HOST_USERNAME}'!")
