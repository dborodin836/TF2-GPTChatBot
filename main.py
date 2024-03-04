from config import init_config

# This is required due to config used in imported modules
init_config()

import uvicorn
import contextlib
import sys
import threading
import time
import tkinter as tk

from pynput import keyboard

from config import config
from modules.bot_state import state_manager
from modules.chat import parse_console_logs_and_build_conversation_history
from modules.commands.gui.openai import gpt3_cmd_handler
from modules.gui.log_window import LogWindow, RedirectStdoutToLogWindow
from modules.logs import get_logger, setup_loggers
from modules.message_queueing import message_queue_handler
from modules.servers.tf2 import get_status
from modules.tf_statistics import StatsData
from modules.server import app

gui_logger = get_logger("gui")


def status_command_sender():
    with contextlib.suppress(Exception):
        while True:
            get_status()
            time.sleep(20)


def keyboard_on_press(key):
    if key == keyboard.Key.f11:
        state_manager.switch_state()
    elif key == keyboard.Key.f10:
        gui_logger.info(StatsData.get_data())


def run_threads():
    root = tk.Tk()
    root.iconphoto(False, tk.PhotoImage(file="icon.png"))
    log_window = LogWindow(root)

    threading.Thread(target=uvicorn.run, daemon=True, args=(app,)).start()
    sys.stdout = RedirectStdoutToLogWindow(log_window)

    setup_loggers()

    threading.Thread(target=parse_console_logs_and_build_conversation_history, daemon=True).start()
    threading.Thread(target=gpt3_cmd_handler, daemon=True).start()
    if config.ENABLE_STATS:
        threading.Thread(target=status_command_sender, daemon=True).start()
    threading.Thread(target=message_queue_handler, daemon=True).start()
    if not config.DISABLE_KEYBOARD_BINDINGS:
        keyboard.Listener(on_press=keyboard_on_press).start()

    log_window.pack()
    root.mainloop()


if __name__ == "__main__":
    run_threads()
