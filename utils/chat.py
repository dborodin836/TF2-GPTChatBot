from typing import Literal

from services.chatgpt import send_gpt_completion_request
from services.network import send_say_command_to_tf2
from utils.text import add_prompts_by_flags
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

    log_message(message_type, username, response)

    send_say_command_to_tf2(response)
    return chat_buffer
