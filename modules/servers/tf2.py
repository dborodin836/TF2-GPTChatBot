import re
import sys
import time
from typing import Generator

from rcon import WrongPassword

from config import config
from modules.logs import get_logger
from modules.message_queueing import message_queue
from modules.rcon_client import RconClient
from modules.typing import QueuedMessage
from modules.utils.text import (
    get_chunk_size,
    get_shortened_username,
    split_into_chunks,
)

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


def check_connection():
    """
    Continuously tries to log in to a remote RCON server using the provided credentials until a
    successful connection is established. If a connection is refused, the function will wait for
    4 seconds and then try again.
    """
    while True:
        try:
            login()
        except ConnectionRefusedError:
            combo_logger.warning("Couldn't connect! Retrying in 4 second...")
            time.sleep(4)
        except Exception as e:
            combo_logger.critical(f"Unknown exception occurred. Retrying in 8 seconds... [{e}]")
            time.sleep(8)
        else:
            combo_logger.info("Successfully connected!")
            break


def get_status():
    while True:
        try:
            with RconClient() as client:
                response = client.run("cmd status")
                return response
        except ConnectionRefusedError:
            main_logger.warning("Failed to fetch status. Connection refused!")
            time.sleep(2)
        except Exception as e:
            main_logger.warning(f"Failed to fetch status. [{e}]")
            time.sleep(2)


def login() -> None:
    """
    Attempts to log in to a remote RCON server using the provided credentials.
    """
    main_logger.debug(
        f"Trying to connect to '{config.RCON_HOST}:{config.RCON_PORT}' with password "
        f"'{config.RCON_PASSWORD[:len(config.RCON_PASSWORD) // 2] + '*' * (len(config.RCON_PASSWORD) // 2)}'"
    )
    with RconClient() as client:
        try:
            client.login(config.RCON_PASSWORD)
        except WrongPassword:
            combo_logger.critical("Passwords do not match!")
            time.sleep(4)
            sys.exit(1)
        except Exception as e:
            combo_logger.error(f"Unhandled exception happened. [{e}]")


def format_say_message(message: str, username: str = None) -> str:
    # Append username to the first chunk
    if username is not None and config.ENABLE_SHORTENED_USERNAMES_RESPONSE:
        message = f"{get_shortened_username(username)}{message}"

    # No " should be in answer it causes say command to broke
    message = message.replace('"', "")

    # Strip the message if needed
    if len(message) > config.HARD_COMPLETION_LIMIT:
        main_logger.warning(
            f"Message is longer than Hard Limit [{len(message)}]. Limit is {config.HARD_COMPLETION_LIMIT}."
        )
        message = message[: config.HARD_COMPLETION_LIMIT] + "..."

    return message


def get_chunks(message: str) -> Generator:
    chunks_size: int = get_chunk_size(message)
    chunks = split_into_chunks(" ".join(message.split()), chunks_size)
    return chunks


def form_say_command(message: str, is_team_chat: bool):
    chunks = get_chunks(message)
    cmd: str = " "

    for chunk in chunks:
        if is_team_chat:
            cmd += f'say_team "{chunk}";wait 1300;'
        else:
            cmd += f'say "{chunk}";wait 1300;'

    return cmd


def send_say_command_to_tf2(message: str, username: str = None, is_team_chat: bool = False) -> None:
    """
    Sends a "say" command to a Team Fortress 2 server using RCON protocol.
    """
    message = format_say_message(message, username)

    msg_chunks = get_chunks(message)

    for msg_chunk in msg_chunks:
        main_logger.trace(f'Adding message "{msg_chunk}" to queue.')
        queued_message = QueuedMessage(text=msg_chunk, is_team_chat=is_team_chat)
        message_queue.put(queued_message)
