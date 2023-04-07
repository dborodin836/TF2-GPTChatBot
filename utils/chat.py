import codecs
import json
import sys
from json import JSONDecodeError
from typing import Literal

from config import GPT_COMMAND, CHATGPT_COMMAND, CLEAR_CHAT_COMMAND
from services.chatgpt import send_gpt_completion_request
from services.network import send_say_command_to_tf2, check_connection
from utils.prompt import load_prompts
from utils.text import add_prompts_by_flags, open_tf2_logfile
from utils.logs import log_message, log_cmd_message

BOT_RUNNING = True
BANNED_PLAYERS = set()

BANS_FILE = 'bans.json'


def handle_gpt_request(message_type: Literal["CHAT", "GPT3"], username: str, user_prompt: str,
                       chat_buffer: str = ""):
    """
    This function is called when the user wants to send a message to the AI chatbot. It logs the
    user's message, and sends a request to GPT-3 to generate a response. Finally, the function
    sends the generated response to the TF2 game.
    """
    log_message(message_type, username, user_prompt)

    message = add_prompts_by_flags(user_prompt)
    if message_type == "CHAT":
        chat_buffer += 'HUMAN:' + message + '\n' + 'AI:'
        message = chat_buffer

    response = send_gpt_completion_request(message, username)

    if message_type == "CHAT":
        chat_buffer += response + '\n'

    log_message(message_type, username, ' '.join(response.split()))

    send_say_command_to_tf2(response)
    return chat_buffer


def load_banned_players() -> set:
    banned_players = set()
    with codecs.open(BANS_FILE, 'r', encoding='utf-8') as f:
        try:
            banned_players = set(json.load(f))
        except (EOFError, JSONDecodeError):
            pass
    return banned_players


def parse_tf2_console() -> None:
    conversation_history: str = ''
    global BOT_RUNNING
    global BANNED_PLAYERS
    check_connection()
    load_prompts()
    print("Ready to use!")
    BANNED_PLAYERS = load_banned_players()

    for line, user in open_tf2_logfile():
        if not BOT_RUNNING:
            continue
        if user in BANNED_PLAYERS:
            continue
        handle_command(line, user, conversation_history)


def handle_command(line: str, user: str, conversation_history: str) -> str:
    global BOT_RUNNING

    if line.strip().startswith(GPT_COMMAND):
        return handle_gpt_request("GPT3", user, line.removeprefix(GPT_COMMAND).strip(),
                                  conversation_history)

    elif line.strip().startswith(CHATGPT_COMMAND):
        return handle_gpt_request("CHAT", user, line.removeprefix(CHATGPT_COMMAND).strip(),
                                  conversation_history)

    elif line.strip().startswith(CLEAR_CHAT_COMMAND):
        log_message("CHAT", user, "CLEARING CHAT")
        return ''

    elif line.strip() == "!gpt_stop":
        BOT_RUNNING = False
        log_cmd_message("BOT STOPPED")
        return conversation_history

    elif line.strip() == "!gpt_start":
        BOT_RUNNING = True
        log_cmd_message("BOT STARTED")
        return conversation_history

    elif line.strip().startswith("ban "):
        name = line.removeprefix("ban ").strip()
        ban_player(name)
        return conversation_history

    elif line.strip().startswith("unban "):
        name = line.removeprefix("unban ").strip()
        unban_player(name)
        return conversation_history

    else:
        return conversation_history


def unban_player(username: str) -> None:
    try:
        BANNED_PLAYERS.remove(username)
    except KeyError:
        pass
    log_cmd_message(f"UNBANNED '{username}'")
    with codecs.open(BANS_FILE, 'w', encoding='utf-8') as f:
        json.dump(list(BANNED_PLAYERS), f)


def ban_player(username: str) -> None:
    BANNED_PLAYERS.add(username)
    log_cmd_message(f"BANNED '{username}'")
    with codecs.open(BANS_FILE, 'w', encoding='utf-8') as f:
        json.dump(list(BANNED_PLAYERS), f)


def handle_gui_console_commands(command: str) -> None:
    global BOT_RUNNING
    global BANNED_PLAYERS

    if command.startswith("stop"):
        BOT_RUNNING = False
        log_cmd_message("BOT STOPPED")

    elif command.startswith("start"):
        BOT_RUNNING = True
        log_cmd_message("BOT STARTED")

    elif command.startswith("quit"):
        sys.exit(0)

    elif command.startswith("ban "):
        name = command.removeprefix("ban ").strip()
        ban_player(name)

    elif command.startswith("unban "):
        name = command.removeprefix("unban ").strip()
        unban_player(name)

    elif command.startswith("bans"):
        if len(BANNED_PLAYERS) == 0:
            print("### NO BANS ###")
        else:
            print("### BANNED PLAYERS ###",
                  *list(BANNED_PLAYERS),
                  sep='\n')

    elif command.startswith("help"):
        print("### HELP ###",
              "start - start the bot",
              "stop - stop the bot",
              "quit - quit the proogram",
              "bans - show all banned players",
              "ban <username> - ban user by username",
              "unban <username> - unban user by username",
              sep='\n')
