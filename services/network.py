from typing import List
import sys
import time

from rcon import WrongPassword
from rcon.source import Client

from config import *
from utils.text import get_chunk_size, get_chunks


def check_connection():
    while True:
        try:
            login()
        except ConnectionRefusedError:
            print("Couldn't connect! Retrying in 4 second...")
            time.sleep(4)
        else:
            print("Successfully connected!")
            break


def login() -> None:
    with Client(RCON_HOST, RCON_PORT, passwd=RCON_PASSWORD) as client:
        try:
            client.login(RCON_PASSWORD)
        except WrongPassword:
            print("Passwords do not match!")
            sys.exit(1)


def send_say_command_to_tf2(message: str) -> None:
    chunks_size: int = get_chunk_size(message)
    chunks: List[str] = get_chunks(" ".join(message.split()), chunks_size)
    cmd: str = ' '

    for chunk in chunks:
        cmd += f'say "{chunk}";wait 1300;'

    with Client(RCON_HOST, RCON_PORT, passwd=RCON_PASSWORD) as client:
        client.run(cmd)
