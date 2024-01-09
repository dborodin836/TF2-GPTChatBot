from config import init_config

# This is required due to config used in imported modules
init_config()

import contextlib
import sys
import threading
import time
import tkinter as tk

import keyboard

from config import config
from modules.gui.log_window import CustomOutput, LogWindow, gpt3_cmd_handler
from modules.services.source_game import get_status, message_queue_handler
from modules.bot_state import switch_state_hotkey_handler
from modules.chat import parse_console_logs_and_build_conversation_history
from modules.logs import get_logger, setup_loggers
from modules.tf_statistics import StatsData

gui_logger = get_logger("gui")


def status_command_sender():
    with contextlib.suppress(Exception):
        while True:
            get_status()
            time.sleep(20)


def get_my_data():
    while True:
        keyboard.wait("F10")
        gui_logger.info(StatsData.get_data())


def run_threads():
    root = tk.Tk()
    log_window = LogWindow(root)
    sys.stdout = CustomOutput(log_window)

    setup_loggers()

    threading.Thread(target=parse_console_logs_and_build_conversation_history, daemon=True).start()
    threading.Thread(target=gpt3_cmd_handler, daemon=True).start()
    threading.Thread(target=switch_state_hotkey_handler, daemon=True).start()
    if config.ENABLE_STATS:
        threading.Thread(target=status_command_sender, daemon=True).start()
    threading.Thread(target=get_my_data, daemon=True).start()
    threading.Thread(target=message_queue_handler, daemon=True).start()

    log_window.pack()
    root.mainloop()


if __name__ == "__main__":
    run_threads()
