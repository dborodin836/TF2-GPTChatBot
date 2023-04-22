import time
from typing import Literal

import openai
import hashlib
from config import config
from services.network import send_say_command_to_tf2
from utils.logs import log_message, log_cmd_message
from utils.text import add_prompts_by_flags


def send_gpt_completion_request(message: str, username: str) -> str:
    openai.api_key = config.OPENAI_API_KEY

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": message}],
        user=hashlib.md5(username.encode()).hexdigest()
    )

    response_text = completion.choices[0].message["content"].strip()
    return response_text


def handle_gpt_request(message_type: Literal["CHAT", "GPT3"], username: str, user_prompt: str,
                       chat_buffer: str = "") -> str:
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

    attempts = 0
    max_attempts = 2

    while attempts < max_attempts:
        try:
            response = send_gpt_completion_request(message, username)
            break
        except openai.error.RateLimitError:
            log_cmd_message("Rate limited! Trying again...")
            time.sleep(2)
            attempts += 1
        except Exception:
            log_cmd_message("Unhandled error happened! Trying again...")
            attempts += 1

    if attempts == max_attempts:
        log_cmd_message("Max number of attempts reached! Try again later!")
        return chat_buffer

    if message_type == "CHAT":
        chat_buffer += response + '\n'

    log_message(message_type, username, ' '.join(response.split()))

    send_say_command_to_tf2(response)
    return chat_buffer
