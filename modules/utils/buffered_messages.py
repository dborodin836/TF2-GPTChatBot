from queue import Queue

from modules.logs import get_logger
from modules.typing import BufferedMessage, BufferedMessageLevel, BufferedMessageType

CONFIG_INIT_MESSAGES_QUEUE: Queue[BufferedMessage] = Queue()

main_logger = get_logger("main")
gui_logger = get_logger("gui")


def buffered_message(
    message: str,
    type_: BufferedMessageType = "GUI",
    level: BufferedMessageLevel = "INFO",
    fail_startup: bool = False,
) -> None:
    CONFIG_INIT_MESSAGES_QUEUE.put(
        BufferedMessage(type=type_, level=level, message=message, fail_startup=fail_startup)
    )


def buffered_fail_message(
    message: str,
    type_: BufferedMessageType = "GUI",
    level: BufferedMessageLevel = "INFO",
):
    buffered_message(message, type_, level, fail_startup=True)


def print_buffered_config_innit_messages() -> None:
    """
    Prints the initialization messages saved in the BUFFERED_CONFIG_INIT_LOG_MESSAGES buffer.
    """
    buffered_messages = list()
    while not CONFIG_INIT_MESSAGES_QUEUE.empty():
        buffered_messages.append(CONFIG_INIT_MESSAGES_QUEUE.get())

    startup_successful = not any(map(lambda x: x.fail_startup, buffered_messages))

    for buffered_message in buffered_messages:
        if buffered_message.type == "GUI":
            gui_logger.log(buffered_message.level, buffered_message.message)
        elif buffered_message.type == "LOG":
            main_logger.log(buffered_message.level, buffered_message.message)
        elif buffered_message.type == "BOTH":
            gui_logger.log(buffered_message.level, buffered_message.message)
            main_logger.log(buffered_message.level, buffered_message.message)

    if startup_successful:
        gui_logger.info("Config is valid!")
        main_logger.info("Config is OK.")
