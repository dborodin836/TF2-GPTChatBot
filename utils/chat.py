import queue

from config import GPT_COMMAND, CHATGPT_COMMAND, CLEAR_CHAT_COMMAND
from services.chatgpt import  handle_gpt_request
from services.network import check_connection
from utils.bans import unban_player, ban_player, load_banned_players, is_banned_username
from utils.commands import handle_rtd_command, stop_bot, start_bot, get_bot_state
from utils.prompt import load_prompts
from utils.text import open_tf2_logfile
from utils.logs import log_message

PROMPTS_QUEUE = queue.Queue()


def parse_tf2_console_logs() -> None:
    conversation_history: str = ''

    check_connection()
    load_prompts()
    load_banned_players()

    print("Ready to use!")

    for line, user in open_tf2_logfile():
        if not get_bot_state():
            continue
        if is_banned_username(user):
            continue
        conversation_history = handle_command(line, user, conversation_history)


def handle_command(line: str, user: str, conversation_history: str) -> str:
    if line.strip().startswith(GPT_COMMAND):
        return handle_gpt_request("GPT3", user, line.removeprefix(GPT_COMMAND).strip(),
                                  conversation_history)

    elif line.strip().startswith(CHATGPT_COMMAND):
        return handle_gpt_request("CHAT", user, line.removeprefix(CHATGPT_COMMAND).strip(),
                                  conversation_history)

    elif line.strip().startswith(CLEAR_CHAT_COMMAND):
        log_message("CHAT", user, "CLEARING CHAT")
        return ''

    elif line.strip().startswith("!rtd"):
        handle_rtd_command(user)

    elif line.strip() == "!gpt_stop":
        stop_bot()

    elif line.strip() == "!gpt_start":
        start_bot()

    elif line.strip().startswith("ban "):
        name = line.removeprefix("ban ").strip()
        ban_player(name)

    elif line.strip().startswith("unban "):
        name = line.removeprefix("unban ").strip()
        unban_player(name)
    return conversation_history
