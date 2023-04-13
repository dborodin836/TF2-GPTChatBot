import sys
import time
import tkinter as tk

import openai

from services.chatgpt import send_gpt_completion_request
from utils.bans import list_banned_players, unban_player, ban_player
from utils.chat import PROMPTS_QUEUE
from utils.commands import print_help_command, start_bot, stop_bot
from utils.logs import log_to_file

PROMPT_PLACEHOLDER = "Type your commands here... Or start with 'help' command"


class LogWindow(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.log_text = None
        self.cmd_line = None
        self.create_widgets()
        self.master.title("TF2-GPTChatBot")
        self.master.resizable(False, False)

    def create_widgets(self):
        # Add a Text widget to the window for displaying logs
        self.log_text = tk.Text(self, height=20, width=100, state="disabled")
        self.log_text.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Add another Text widget below the log_text widget for displaying additional text
        self.cmd_line = tk.Text(self, height=1, width=100)
        self.cmd_line.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.cmd_line.bind("<Return>", self.handle_commands)

        # Add a placeholder to the additional_text widget
        self.cmd_line.insert("1.0", PROMPT_PLACEHOLDER)

        # Binds to make the placeholder work
        self.cmd_line.bind("<FocusIn>", self.handle_additional_text_focus_in)
        self.cmd_line.bind("<FocusOut>", self.handle_additional_text_focus_out)

    def update_logs(self, message):
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, f"{message}")
        self.log_text.config(state="disabled")
        self.log_text.see(tk.END)  # Scroll to the end of the text widget

    def exit_program(self):
        self.master.destroy()

    def handle_commands(self, event):
        text = self.cmd_line.get("1.0", tk.END).strip()

        if text.strip == "":
            return

        handle_gui_console_commands(text)

        # Clear the additional_text widget after the function is executed
        self.cmd_line.delete("1.0", tk.END)

    def handle_additional_text_focus_in(self, event):
        # Clear the placeholder text when the additional_text widget receives focus
        if self.cmd_line.get("1.0", tk.END).strip() == PROMPT_PLACEHOLDER:
            self.cmd_line.delete("1.0", tk.END)

    def handle_additional_text_focus_out(self, event):
        # Show the placeholder text when the additional_text widget loses focus and is empty
        if not self.cmd_line.get("1.0", tk.END).strip():
            self.cmd_line.insert("1.0", PROMPT_PLACEHOLDER)


class CustomOutput:
    def __init__(self, window: LogWindow):
        self.window = window

    def write(self, message):
        self.window.update_logs(message)
        log_to_file(message)

    def flush(self):
        ...


def handle_gui_console_commands(command: str) -> None:
    if command.startswith("stop"):
        stop_bot()

    elif command.startswith("start"):
        start_bot()

    elif command.startswith("quit"):
        sys.exit(0)

    elif command.startswith("ban "):
        name = command.removeprefix("ban ").strip()
        ban_player(name)

    elif command.startswith("unban "):
        name = command.removeprefix("unban ").strip()
        unban_player(name)

    elif command.startswith("gpt3 "):
        prompt = command.removeprefix("gpt3 ").strip()
        PROMPTS_QUEUE.put(prompt)

    elif command.startswith("bans"):
        list_banned_players()

    elif command.startswith("help"):
        print_help_command()


def gpt3_cmd_handler():
    while True:
        if PROMPTS_QUEUE.qsize() != 0:
            prompt = PROMPTS_QUEUE.get()
            try:
                response = send_gpt_completion_request(prompt, "admin")
                print(response)
            except openai.error.RateLimitError:
                print("Rate Limited! Try again later.")
        else:
            time.sleep(2)
