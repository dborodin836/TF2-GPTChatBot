from config import init_config
# This is required due to config used in imported modules
init_config()

import sys
import tkinter as tk
import threading

from gui.log_window import LogWindow, CustomOutput, gpt3_cmd_handler
from utils.chat import parse_tf2_console_logs


def run_threads():
    root = tk.Tk()
    log_window = LogWindow(root)
    sys.stdout = CustomOutput(log_window)

    t1 = threading.Thread(target=parse_tf2_console_logs, daemon=True)
    t2 = threading.Thread(target=gpt3_cmd_handler, daemon=True)
    t1.start()
    t2.start()

    log_window.pack()
    root.mainloop()


if __name__ == '__main__':
    run_threads()
