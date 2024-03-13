from config import init_config

# This is required due to config used in imported modules
init_config()

import argparse
import contextlib
import sys
import threading
import time
import tkinter as tk

import uvicorn
from pynput import keyboard

from config import config
from modules.bot_state import state_manager
from modules.chat import parse_console_logs_and_build_conversation_history
from modules.commands.gui.openai import gpt3_cmd_handler
from modules.gui.log_window import LogWindow, RedirectStdoutToLogWindow
from modules.logs import get_logger, setup_loggers
from modules.message_queueing import message_queue_handler
from modules.server import app
from modules.servers.tf2 import get_status
from modules.tf_statistics import StatsData

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


def run_common_threads():
    if config.ENABLE_STATS:
        threading.Thread(target=status_command_sender, daemon=True).start()

    if not config.DISABLE_KEYBOARD_BINDINGS:
        keyboard.Listener(on_press=keyboard_on_press).start()

    threading.Thread(target=message_queue_handler, daemon=True).start()
    threading.Thread(target=gpt3_cmd_handler, daemon=True).start()


def run_threads(args: argparse.Namespace):
    if args.web_server:
        print("Starting in web server mode.")
        threading.Thread(target=uvicorn.run, daemon=True, args=(app,)).start()

    if args.no_gui:
        print("Running without GUI.")
        parse_console_logs_and_build_conversation_history()
    else:
        root = tk.Tk()
        root.iconphoto(False, tk.PhotoImage(file="icon.png"))
        log_window = LogWindow(root)
        sys.stdout = RedirectStdoutToLogWindow(log_window)

        setup_loggers()
        run_common_threads()

        threading.Thread(target=parse_console_logs_and_build_conversation_history, daemon=True).start()

        log_window.pack()
        root.mainloop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='An AI-powered chatbot for Team Fortress 2 fans and players.')

    parser.add_argument('--no-gui', action='store_true',
                        help='Run the application without the GUI.')
    parser.add_argument('--web-server', action='store_true',
                        help='Start the application in web server mode.')

    print(parser.parse_args())
    run_threads(parser.parse_args())

    # TODO: no display to server with --no-gui
    # TODO: frontend sending /settings twice
