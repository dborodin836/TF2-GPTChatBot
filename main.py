from config import *
import tkinter as tk
import threading

from gui.log_window import LogWindow, CustomOutput
from utils.chat import parse_tf2_console


def run_threads():
    root = tk.Tk()
    log_window = LogWindow(root)

    sys.stdout = CustomOutput(log_window)

    t1 = threading.Thread(target=parse_tf2_console, daemon=True)
    # t2 = threading.Thread(target=test1, daemon=True)
    t1.start()
    # t2.start()

    log_window.pack()
    root.mainloop()


if __name__ == '__main__':
    run_threads()
