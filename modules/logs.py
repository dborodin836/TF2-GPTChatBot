import sys
from datetime import datetime as dt

from loguru import logger

FORMAT_LINE_MAIN = (
    "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} | {message}"
)
FORMAT_LINE_GUI = "{time:YYYY-MM-DD HH:mm:ss.SSS} | {message}"

__main_logger = logger.bind(name="main")
__gui_logger = logger.bind(name="gui")
__combo_logger = logger.bind(name="combo")


class LoggerDontExist(Exception): ...


def get_logger(name: str):
    if name == "main":
        return __main_logger
    elif name == "gui":
        return __gui_logger
    elif name == "combo":
        return __combo_logger
    else:
        raise LoggerDontExist("Specified logger doesn't exist!")


def make_name_filter(name):
    def filter(record):
        return record["extra"].get("name") == name

    return filter


def setup_loggers():
    __main_logger.remove()
    __gui_logger.remove()
    __combo_logger.remove()

    __main_logger.add(
        "logs/log-{time:YYYY-MM-DD}.log",
        mode="a",
        format=FORMAT_LINE_MAIN,
        level="DEBUG",
        filter=make_name_filter("main"),
        retention="1 week",
        rotation="50 MB",
    )

    __gui_logger.add(sys.stdout, format="{message}", filter=make_name_filter("gui"))
    __gui_logger.add(
        "logs/log-gui-{time:YYYY-MM-DD}.log",
        mode="a",
        format=FORMAT_LINE_GUI,
        level="DEBUG",
        filter=make_name_filter("gui"),
        retention="1 week",
        rotation="50 MB",
    )

    __combo_logger.add(sys.stdout, format="{message}", filter=make_name_filter("combo"))
    __combo_logger.add(
        "logs/log-{time:YYYY-MM-DD}.log",
        mode="a",
        format=FORMAT_LINE_MAIN,
        level="TRACE",
        filter=make_name_filter("combo"),
        retention="1 week",
        rotation="50 MB",
    )


def get_time_stamp() -> str:
    """
    Returns the current time as a string in the format "HH:MM:SS".
    """
    return f"{dt.now().strftime('%H:%M:%S')}"


def log_gui_model_message(type_: str, username: str, message: str) -> None:
    """
    Logs a message with the current timestamp, message type, username, user_id, and prompt text.
    """
    if message:
        log_msg = f"[{get_time_stamp()}] ({type_}) User: '{username}' --- '{message}'"
    else:
        log_msg = f"[{get_time_stamp()}] ({type_}) User: '{username}'"
    __gui_logger.info(log_msg)


def log_gui_general_message(message: str) -> None:
    log_msg = f"[{get_time_stamp()}] -- {message}"
    __gui_logger.info(log_msg)
