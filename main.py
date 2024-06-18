from config import init_config

# This is required due to config used in imported modules
init_config()

import sys
import threading
import tkinter as tk

from pynput import keyboard

from config import config
from modules.bot_state import state_manager
from modules.chat import parse_console_logs_and_build_conversation_history
from modules.commands.gui.openai import gpt3_cmd_handler
from modules.gui.log_window import LogWindow, RedirectStdoutToLogWindow
from modules.lobby_manager import lobby_manager
from modules.logs import get_logger, setup_loggers
from modules.message_queueing import message_queue_handler

gui_logger = get_logger("gui")


def keyboard_on_press(key):
    if key == keyboard.Key.f11:
        state_manager.switch_state()
    elif key == keyboard.Key.f10:
        gui_logger.info(lobby_manager.get_data())


def run_threads():
    root = tk.Tk()
    root.iconphoto(False, tk.PhotoImage(file="icon.png"))
    log_window = LogWindow(root)
    sys.stdout = RedirectStdoutToLogWindow(log_window)

    setup_loggers()

    threading.Thread(target=parse_console_logs_and_build_conversation_history, daemon=True).start()
    threading.Thread(target=gpt3_cmd_handler, daemon=True).start()
    threading.Thread(target=message_queue_handler, daemon=True).start()
    if not config.DISABLE_KEYBOARD_BINDINGS:
        keyboard.Listener(on_press=keyboard_on_press).start()

    log_window.pack()
    root.mainloop()


if __name__ == "__main__":
    run_threads()
