import time
import sys
import re

from rcon import WrongPassword
from rcon.source import Client

from config import config
from utils.text import get_chunk_size, get_chunks


def get_username() -> str:
    with Client(config.RCON_HOST, config.RCON_PORT, passwd=config.RCON_PASSWORD) as client:
        response = client.run('name')

    pattern = r'"name"\s*=\s"(.+?)"'

    match = re.search(pattern, response)

    if match:
        name = match.group(1)
        return name


def check_connection():
    """
    Continuously tries to login to a remote RCON server using the provided credentials until a
    successful connection is established. If a connection is refused, the function will wait for
    4 seconds and then try again.
    """
    while True:
        try:
            login()
        except ConnectionRefusedError:
            print("Couldn't connect! Retrying in 4 second...")
            time.sleep(4)
        else:
            print("Successfully connected!")
            break


def get_status():
    while True:
        try:
            with Client(config.RCON_HOST, config.RCON_PORT, passwd=config.RCON_PASSWORD) as client:
                response = client.run('cmd status')
                return response
        except ConnectionRefusedError:
            time.sleep(2)


def login() -> None:
    """
    Attempts to login to a remote RCON server using the provided credentials.
    """
    with Client(config.RCON_HOST, config.RCON_PORT, passwd=config.RCON_PASSWORD) as client:
        try:
            client.login(config.RCON_PASSWORD)
        except WrongPassword:
            print("Passwords do not match!")
            sys.exit(1)


def send_say_command_to_tf2(message: str, team_chat: bool = False) -> None:
    """
    Sends a "say" command to a Team Fortress 2 server using RCON protocol.
    """
    chunks_size: int = get_chunk_size(message)

    # No " should be in answer it causes say command to broke
    message = message.replace('"', '')

    if len(message) > config.HARD_COMPLETION_LIMIT:
        message = message[:config.HARD_COMPLETION_LIMIT] + '...'

    chunks = get_chunks(" ".join(message.split()), chunks_size)
    cmd: str = ' '

    for chunk in chunks:
        if team_chat:
            cmd += f'say_team "{chunk}";wait 1300;'
        else:
            cmd += f'say "{chunk}";wait 1300;'

    with Client(config.RCON_HOST, config.RCON_PORT, passwd=config.RCON_PASSWORD) as client:
        client.run(cmd)
