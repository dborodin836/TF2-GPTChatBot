from typing import Literal

from config import GPT_COMMAND, CHATGPT_COMMAND, CLEAR_CHAT_COMMAND
from services.chatgpt import send_gpt_completion_request
from services.network import send_say_command_to_tf2, check_connection
from utils.prompt import load_prompts
from utils.text import add_prompts_by_flags, open_tf2_logfile
from utils.logs import log_message


def handle_gpt_request(message_type: Literal["CHAT", "GPT3"], username: str, user_prompt: str,
                       chat_buffer: str = None):
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


def parse_tf2_console() -> None:
    # Initialize conversation history
    conversation_history = ''

    check_connection()

    # Load prompts from .xtx files
    load_prompts()
    print("Ready to use!")

    # Loop through log file
    for line, user in open_tf2_logfile():
        # Handle GPT3 completion requests
        if line.strip().startswith(GPT_COMMAND):
            prompt = line.removeprefix(GPT_COMMAND).strip()
            conversation_history = handle_gpt_request("GPT3", user, prompt, conversation_history)

        # Handle ChatGPT requests
        if line.strip().startswith(CHATGPT_COMMAND):
            prompt = line.removeprefix(CHATGPT_COMMAND).strip()
            conversation_history = handle_gpt_request("CHAT", user, prompt, conversation_history)

        # Handle clear chat requests
        if line.strip().startswith(CLEAR_CHAT_COMMAND):
            log_message("CHAT", user, "CLEARING CHAT")
            conversation_history = ''


def handle_gui_console_commands(command):
    print(command)
