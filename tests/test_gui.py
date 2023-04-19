import os
import tkinter as tk
import pytest

from gui.log_window import LogWindow


@pytest.fixture
def log_window():
    os.system('Xvfb :1 -screen 0 1600x1200x16  &')
    os.environ['DISPLAY'] = ':1.0'
    root = tk.Tk()
    return LogWindow(master=root)


def test_update_logs(log_window):
    log_window.update_logs("test message")
    assert log_window.log_text.get("1.0", "end-1c") == "test message"
