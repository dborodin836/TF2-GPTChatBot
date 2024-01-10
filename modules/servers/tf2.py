import re
import sys
import time
import queue
from typing import Generator, Optional

from rcon import WrongPassword

from config import config
from modules.logs import get_logger
from modules.rcon_client import RconClient
from modules.utils.text import get_chunk_size, split_into_chunks, get_shortened_username, has_cyrillic
from modules.types import QueuedMessage

main_logger = get_logger("main")
gui_logger = get_logger("gui")
combo_logger = get_logger("combo")

message_queue = queue.Queue()


class ConfirmableQueueManager:
    queue: queue.Queue
    is_locked: bool = False
    awaiting_message: Optional[str] = None
    last_confirmed_message: float
    warning_sent = False

    def __init__(self, q):
        self.queue = q

    def clean(self):
        self.queue = queue.Queue()
        self.is_locked = False
        self.awaiting_message = None
        self.last_confirmed_message = time.time()
        self.warning_sent = False

    def start_worker(self):
        while True:
            if self.is_locked:
                time.sleep(0.5)
                if time.time() - self.last_confirmed_message > 30:
                    combo_logger.debug("Queue seems to be dead. Cleaning...")
                    self.clean()
                elif time.time() - self.last_confirmed_message > 15:
                    queued_message: QueuedMessage = self.queue.queue[0]
                    send_say_cmd(queued_message)
                elif time.time() - self.last_confirmed_message > 10:
                    if not self.warning_sent:
                        combo_logger.debug("You're likely to be muted by tf2.")
                        self.warning_sent = True
                continue

            if not self.queue.empty():
                queued_message: QueuedMessage = self.queue.queue[0]
                if has_cyrillic(queued_message.text):
                    self.awaiting_message = queued_message.text[:len(queued_message.text) // 2]
                else:
                    self.awaiting_message = queued_message.text
                self.is_locked = True
                main_logger.debug("Locking queue")
                self.last_confirmed_message = time.time()
                send_say_cmd(queued_message)
            else:
                time.sleep(0.5)

    def unlock_queue(self) -> None:
        main_logger.debug("Unlocking queue")
        self.queue.get()
        time.time()
        self.awaiting_message = None
        self.is_locked = False
        self.warning_sent = False
        self.last_confirmed_message = time.time()

    def get_awaited_msg(self) -> str:
        if self.awaiting_message is not None:
            main_logger.trace(f"Requested awaited message '{self.awaiting_message}'")
        return self.awaiting_message


q_manager = ConfirmableQueueManager(message_queue)


def message_queue_handler() -> None:
    if not config.CONFIRMABLE_QUEUE:
        while True:
            if not message_queue.empty():
                queued_message: QueuedMessage = message_queue.get()
                main_logger.trace(f"Retrieved message '{queued_message.text}' from queue")

                send_say_cmd(queued_message)
            else:
                time.sleep(0.5)
    else:
        q_manager.start_worker()


def send_say_cmd(queued_message):
    if queued_message.is_team_chat:
        cmd = f'say_team "{queued_message.text}";'
    else:
        cmd = f'say "{queued_message.text}";'

    with RconClient() as client:
        try:
            main_logger.debug(f"Sending command [{cmd}]")
            client.run(cmd)
        except Exception as e:
            main_logger.error(f"Unhandled exception happened. [{e}]")
    time.sleep(config.DELAY_BETWEEN_MESSAGES)


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
            f"Message is longer than Hard Limit [{len(message)}]. Limit is {config.HARD_COMPLETION_LIMIT}.")
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
