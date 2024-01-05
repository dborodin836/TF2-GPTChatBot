import re
import sys
import time

from rcon import WrongPassword
from rcon.source import Client

from config import config
from utils.logs import get_logger
from utils.text import get_chunk_size, get_chunks, get_shortened_username

main_logger = get_logger("main")
gui_logger = get_logger("gui")
combo_logger = get_logger("combo")


def get_username() -> str:
    try:
        with Client(config.RCON_HOST, config.RCON_PORT, passwd=config.RCON_PASSWORD) as client:
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
            with Client(config.RCON_HOST, config.RCON_PORT, passwd=config.RCON_PASSWORD) as client:
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
    with Client(config.RCON_HOST, config.RCON_PORT, passwd=config.RCON_PASSWORD) as client:
        try:
            client.login(config.RCON_PASSWORD)
        except WrongPassword:
            combo_logger.critical("Passwords do not match!")
            time.sleep(4)
            sys.exit(1)
        except Exception as e:
            combo_logger.error(f"Unhandled exception happened. [{e}]")


def send_say_command_to_tf2(message: str, username: str = None, team_chat: bool = False) -> None:
    """
    Sends a "say" command to a Team Fortress 2 server using RCON protocol.
    """

    # Append username to the first chunk
    if username is not None and config.ENABLE_SHORTENED_USERNAMES_RESPONSE:
        message = f"[{get_shortened_username(username)}] {message}"

    chunks_size: int = get_chunk_size(message)

    # No " should be in answer it causes say command to broke
    message = message.replace('"', "")

    if len(message) > config.HARD_COMPLETION_LIMIT:
        main_logger.warning(
            f"Message is longer than Hard Limit [{len(message)}]. Limit is {config.HARD_COMPLETION_LIMIT}.")
        message = message[: config.HARD_COMPLETION_LIMIT] + "..."

    chunks = get_chunks(" ".join(message.split()), chunks_size)
    cmd: str = " "

    for chunk in chunks:
        if team_chat:
            cmd += f'say_team "{chunk}";wait 1300;'
        else:
            cmd += f'say "{chunk}";wait 1300;'

        with Client(config.RCON_HOST, config.RCON_PORT, passwd=config.RCON_PASSWORD) as client:
            try:
                client.run(cmd)
            except Exception as e:
                main_logger.error(f"Unhandled exception happened. [{e}]")
