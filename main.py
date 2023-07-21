from config import init_config
# This is required due to config used in imported modules
init_config()

import sys
import threading
import time
import tkinter as tk
import asyncio

# Global reference to loop allows access from different environments.
from gui.log_window import CustomOutput, LogWindow
from utils.chat import parse_console_logs_and_build_conversation_history
from aio import aio_main, get_loop


def tk_main():
    root = tk.Tk()
    log_window = LogWindow(root)
    sys.stdout = CustomOutput(log_window)

    # The asyncio loop must start before the tkinter event loop.
    while not get_loop():
        time.sleep(0)

    asyncio.run_coroutine_threadsafe(parse_console_logs_and_build_conversation_history(), get_loop())

    log_window.pack()
    root.mainloop()


def main():
    aio_initiate_shutdown = threading.Event()
    aio_thread = threading.Thread(target=aio_main, args=(aio_initiate_shutdown,))
    aio_thread.start()

    tk_main()

    # Close the asyncio permanent loop and join the thread in which it runs.
    aio_initiate_shutdown.set()
    aio_thread.join()


if __name__ == '__main__':
    sys.exit(main())