import datetime
from typing import Literal
from datetime import datetime as dt

DATE = None


def get_time_stamp():
    return f"{dt.now().strftime('%H:%M:%S')}"


def log_message(message_type: Literal["CHAT", "GPT3"], username: str, user_prompt: str) -> None:
    """
    Logs a message with the current timestamp, message type, username, user_id, and prompt text.
    """
    log_msg = f"[{get_time_stamp()}] ({message_type}) User: '{username}' --- '{user_prompt}'"
    print(log_msg)


def log_cmd_message(message: str) -> None:
    log_msg = f"[{get_time_stamp()}] -- {message}"
    print(log_msg)


def log_to_file(mes):
    global DATE
    if DATE is None:
        DATE = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    filename = f"log_{DATE}.txt"
    with open(filename, "a") as f:
        f.write(mes)