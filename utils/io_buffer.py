from config import CONFIG_INIT_MESSAGES_QUEUE
from utils.logs import get_logger

gui_logger = get_logger("gui")
main_logger = get_logger("main")


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
        gui_logger.info("Ready to use!")
        main_logger.info("Config is OK.")
    else:
        gui_logger.error(
            "App is not configured correctly. Check documentation and edit config.ini file."
        )
        main_logger.error("Config is faulty.")
