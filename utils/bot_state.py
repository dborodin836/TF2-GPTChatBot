import keyboard

from utils.logs import log_gui_general_message, get_logger

main_logger = get_logger("main")

_BOT_RUNNING = True
SWITCH_STATE_HOTKEY = "F11"


def start_bot() -> None:
    global _BOT_RUNNING
    _BOT_RUNNING = True
    main_logger.info("Bot started.")
    log_gui_general_message("BOT STARTED")


def stop_bot() -> None:
    global _BOT_RUNNING
    _BOT_RUNNING = False
    main_logger.info("Bot stopped.")
    log_gui_general_message("BOT STOPPED")


def get_bot_state() -> bool:
    return _BOT_RUNNING


def switch_state() -> None:
    if get_bot_state():
        stop_bot()
    else:
        start_bot()


def switch_state_hotkey_handler() -> None:
    while True:
        keyboard.wait(SWITCH_STATE_HOTKEY)
        switch_state()
