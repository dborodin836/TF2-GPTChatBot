from modules.bot_state import stop_bot, start_bot


def handle_stop(command, shared_dict):
    stop_bot()


def handle_start(command, shared_dict):
    start_bot()
