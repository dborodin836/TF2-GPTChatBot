import tkinter as tk
import pytest

from gui.log_window import LogWindow


@pytest.fixture
def log_window():
    root = tk.Tk()
    return LogWindow(master=root)


def test_update_logs(log_window):
    log_window.update_logs("test message")
    assert log_window.log_text.get("1.0", "end-1c") == "test message"
