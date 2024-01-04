import sys
from datetime import datetime as dt

from loguru import logger

FORMAT_LINE_MAIN = "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} | {message}"
FORMAT_LINE_GUI = "{time:YYYY-MM-DD HH:mm:ss.SSS} | {message}"

main_logger = logger.bind(name="main")
gui_logger = logger.bind(name="gui")
combo_logger = logger.bind(name="combo")


class LoggerDontExist(Exception):
    ...


def get_logger(name: str):
    if name == "main":
        return main_logger
    elif name == "gui":
        return gui_logger
    elif name == "combo":
        return combo_logger
    else:
        raise LoggerDontExist("Specified logger doesn't exist!")


def make_name_filter(name):
    def filter(record):
        return record["extra"].get("name") == name

    return filter


def setup_loggers():
    main_logger.remove()
    gui_logger.remove()
    combo_logger.remove()

    main_logger.add(
        "logs/log-{time:YYYY-MM-DD}.log",
        mode="a",
        format=FORMAT_LINE_MAIN,
        level="DEBUG",
        filter=make_name_filter("main"),
        retention="1 week",
        rotation="50 MB"
    )

    gui_logger.add(sys.stdout, format="{message}", filter=make_name_filter("gui"))
    gui_logger.add(
        "logs/log-gui-{time:YYYY-MM-DD}.log",
        mode="a",
        format=FORMAT_LINE_GUI,
        level="DEBUG",
        filter=make_name_filter("gui"),
        retention="1 week",
        rotation="50 MB"
    )

    combo_logger.add(sys.stdout, format="{message}", filter=make_name_filter("combo"))
    combo_logger.add(
        "logs/log-{time:YYYY-MM-DD}.log",
        mode="a",
        format=FORMAT_LINE_MAIN,
        level="DEBUG",
        filter=make_name_filter("combo"),
        retention="1 week",
        rotation="50 MB"
    )


def get_time_stamp() -> str:
    """
    Returns the current time as a string in the format "HH:MM:SS".
    """
    return f"{dt.now().strftime('%H:%M:%S')}"


def log_gui_model_message(message_type: str, username: str, user_prompt: str) -> None:
    """
    Logs a message with the current timestamp, message type, username, user_id, and prompt text.
    """
    log_msg = f"[{get_time_stamp()}] ({message_type}) User: '{username}' --- '{user_prompt}'"
    gui_logger.info(log_msg)


def log_gui_general_message(message: str) -> None:
    log_msg = f"[{get_time_stamp()}] -- {message}"
    gui_logger.info(log_msg)
