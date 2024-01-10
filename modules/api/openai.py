import hashlib
import re
import time

import openai

from config import config
from modules.logs import get_logger, log_gui_general_message, log_gui_model_message
from modules.servers.tf2 import send_say_command_to_tf2
from modules.typing import MessageHistory
from modules.utils.text import add_prompts_by_flags

main_logger = get_logger("main")
gui_logger = get_logger("gui")


def is_violated_tos(message: str) -> bool:
    openai.api_key = config.OPENAI_API_KEY
    try:
        response = openai.Moderation.create(
            input=message,
        )
    except openai.error.APIError:
        main_logger.error(f"Failed to moderate message. [APIError]")
        return True
    except Exception as e:
        main_logger.error(f"Failed to moderate message. [{e}]")
        return True

    return response.results[0]["flagged"]


def send_gpt_completion_request(
    conversation_history: MessageHistory, username: str, model: str
) -> str:
    openai.api_key = config.OPENAI_API_KEY

    completion = openai.ChatCompletion.create(
        model=model, messages=conversation_history, user=hashlib.md5(username.encode()).hexdigest()
    )

    response_text = completion.choices[0].message["content"].strip()
    return response_text


def handle_cgpt_request(
    username: str,
    user_prompt: str,
    conversation_history: MessageHistory,
    model,
    is_team: bool = False,
) -> MessageHistory:
    """
    This function is called when the user wants to send a message to the AI chatbot. It logs the
    user's message, and sends a request to GPT-3 to generate a response. Finally, the function
    sends the generated response to the TF2 game.
    """
    log_gui_model_message(model.upper(), username, user_prompt)

    message = add_prompts_by_flags(user_prompt)

    if not config.TOS_VIOLATION and is_violated_tos(message) and config.HOST_USERNAME != username:
        gui_logger.error(f"Request '{user_prompt}' violates OPENAI TOS. Skipping...")
        return conversation_history

    conversation_history.append({"role": "user", "content": message})

    response = get_response(conversation_history, username, model)

    if response:
        conversation_history.append({"role": "assistant", "content": response})
        log_gui_model_message(model.upper(), username, " ".join(response.split()))
        send_say_command_to_tf2(response, username, is_team)

    return conversation_history


def handle_gpt_request(
    username: str, user_prompt: str, model: str, is_team_chat: bool = False
) -> None:
    """
    This function is called when the user wants to send a message to the AI chatbot. It logs the
    user's message, and sends a request to GPT-3 to generate a response. Finally, the function
    sends the generated response to the TF2 game.
    """
    log_gui_model_message(model, username, user_prompt)

    message = add_prompts_by_flags(user_prompt)

    if not config.TOS_VIOLATION and is_violated_tos(message) and config.HOST_USERNAME != username:
        gui_logger.warning(
            f"Request '{user_prompt}' by user {username} violates OPENAI TOS. Skipping..."
        )
        return

    response = get_response([{"role": "user", "content": message}], username, model)

    if response:
        main_logger.info(
            f"Got response for user {username}. Response: {' '.join(response.split())}"
        )
        log_gui_model_message(model, username, " ".join(response.split()))
        send_say_command_to_tf2(response, username, is_team_chat)


def get_response(conversation_history: MessageHistory, username: str, model) -> str | None:
    attempts = 0
    max_attempts = 2

    while attempts < max_attempts:
        try:
            response = send_gpt_completion_request(conversation_history, username, model=model)
            filtered_response = remove_hashtags(response)
            return filtered_response
        except openai.error.RateLimitError:
            log_gui_general_message("Rate limited! Trying again...")
            main_logger(f"User is rate limited.")
            time.sleep(2)
            attempts += 1
        except openai.error.APIError as e:
            log_gui_general_message(f"Wasn't able to connect to OpenAI API. Cancelling...")
            main_logger.error(f"APIError happened. [{e}]")
            return
        except Exception as e:
            log_gui_general_message(f"Unhandled error happened! Cancelling ({e})")
            main_logger(f"Unhandled error happened! Cancelling ({e})")
            return

    if attempts == max_attempts:
        log_gui_general_message("Max number of attempts reached! Try again later!")
        main_logger(f"Max number of attempts reached. [{max_attempts}/{max_attempts}]")


def remove_hashtags(text: str) -> str:
    """
    Removes hashtags from a given string.
    """
    cleaned_text = re.sub(r"#\w+", "", text).strip()
    return cleaned_text
