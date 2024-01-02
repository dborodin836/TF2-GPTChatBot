import codecs
import os
from typing import Literal
from datetime import datetime as dt

DATE = None


def get_time_stamp() -> str:
    """
    Returns the current time as a string in the format "HH:MM:SS".
    """
    return f"{dt.now().strftime('%H:%M:%S')}"


def log_message(message_type: Literal["CHAT", "GPT3", "CUSTOM"], username: str, user_prompt: str) -> None:
    """
    Logs a message with the current timestamp, message type, username, user_id, and prompt text.
    """
    log_msg = f"[{get_time_stamp()}] ({message_type}) User: '{username}' --- '{user_prompt}'"
    print(log_msg)


def log_cmd_message(message: str) -> None:
    log_msg = f"[{get_time_stamp()}] -- {message}"
    print(log_msg)


def log_to_file(message: str, path: str = None) -> None:
    """
    Appends the given message to a log file with a timestamp.
    """
    global DATE
    if DATE is None:
        DATE = dt.now().strftime('%Y-%m-%d_%H-%M-%S')

    if not os.path.exists("logs"):
        os.makedirs("logs")

    filename = path or f"logs/log_{DATE}.txt"
    with codecs.open(filename, "a", encoding="utf-8") as f:
        f.write(message)
