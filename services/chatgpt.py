import re
import time

import openai
import hashlib
from config import config
from services.source_game import send_say_command_to_tf2
from utils.logs import log_message, log_cmd_message
from utils.text import add_prompts_by_flags
from utils.types import MessageHistory


def is_violated_tos(message: str) -> bool:
    openai.api_key = config.OPENAI_API_KEY
    response = openai.Moderation.create(
        input=message,
    )

    return response.results[0]['flagged']


def send_gpt_completion_request(conversation_history: MessageHistory, username: str) -> str:
    openai.api_key = config.OPENAI_API_KEY

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation_history,
        user=hashlib.md5(username.encode()).hexdigest()
    )

    response_text = completion.choices[0].message["content"].strip()
    return response_text


def handle_cgpt_request(username: str, user_prompt: str, conversation_history: MessageHistory,
                        is_team: bool = False) -> MessageHistory:
    """
    This function is called when the user wants to send a message to the AI chatbot. It logs the
    user's message, and sends a request to GPT-3 to generate a response. Finally, the function
    sends the generated response to the TF2 game.
    """
    log_message("CHAT", username, user_prompt)

    message = add_prompts_by_flags(user_prompt)

    if not config.TOS_VIOLATION:
        if is_violated_tos(message):
            if config.HOST_USERNAME != username:
                print(f"Request '{user_prompt}' violates OPENAI TOS. Skipping...")
                return MessageHistory

    conversation_history.append({"role": "user", "content": message})

    response = get_response(conversation_history, username)

    if response:
        conversation_history.append({"role": "assistant", "content": response})
        log_message("GPT3", username, ' '.join(response.split()))
        send_say_command_to_tf2(response, is_team)

    return conversation_history


def handle_gpt_request(username: str, user_prompt: str, is_team: bool = False) -> None:
    """
    This function is called when the user wants to send a message to the AI chatbot. It logs the
    user's message, and sends a request to GPT-3 to generate a response. Finally, the function
    sends the generated response to the TF2 game.
    """
    log_message("GPT3", username, user_prompt)

    message = add_prompts_by_flags(user_prompt)

    if not config.TOS_VIOLATION:
        if is_violated_tos(message):
            if config.HOST_USERNAME != username:
                print(f"Request '{user_prompt}' violates OPENAI TOS. Skipping...")
                return

    response = get_response([{"role": "user", "content": message}], username)

    if response:
        log_message("GPT3", username, ' '.join(response.split()))
        send_say_command_to_tf2(response, is_team)


def get_response(conversation_history: MessageHistory, username: str) -> str | None:
    attempts = 0
    max_attempts = 2

    while attempts < max_attempts:
        try:
            response = send_gpt_completion_request(conversation_history, username)
            filtered_response = remove_hashtags(response)
            return filtered_response
        except openai.error.RateLimitError:
            log_cmd_message("Rate limited! Trying again...")
            time.sleep(2)
            attempts += 1
        except Exception as e:
            log_cmd_message(f"Unhandled error happened! Trying again... ({e})")
            attempts += 1

    if attempts == max_attempts:
        log_cmd_message("Max number of attempts reached! Try again later!")
        return


def remove_hashtags(text: str) -> str:
    """
    Removes hashtags from a given string.
    """
    cleaned_text = re.sub(r'#\w+', '', text).strip()
    return cleaned_text
