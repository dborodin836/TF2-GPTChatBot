import hashlib
import time

import openai

from config import config
from modules.conversation_history import ConversationHistory
from modules.logs import get_logger, log_gui_general_message, log_gui_model_message
from modules.servers.tf2 import send_say_command_to_tf2
from modules.typing import Message, MessageHistory
from modules.utils.text import get_system_message, remove_args, remove_hashtags

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
        model=model,
        messages=conversation_history,
        user=hashlib.md5(username.encode()).hexdigest(),
    )

    response_text = completion.choices[0].message["content"].strip()
    return response_text


def handle_cgpt_request(
    username: str,
    user_prompt: str,
    conversation_history: ConversationHistory,
    model,
    is_team: bool = False,
) -> ConversationHistory:
    """
    This function is called when the user wants to send a message to the AI chatbot. It logs the
    user's message, and sends a request to generate a response.
    """
    log_gui_model_message(model, username, user_prompt)

    user_message = remove_args(user_prompt)
    if (
        not config.TOS_VIOLATION
        and is_violated_tos(user_message)
        and config.HOST_USERNAME != username
    ):
        gui_logger.error(f"Request '{user_prompt}' violates OPENAI TOS. Skipping...")
        return conversation_history

    conversation_history.add_user_message_from_prompt(user_prompt)

    response = get_response(conversation_history.get_messages_array(), username, model)

    if response:
        conversation_history.add_assistant_message(Message(role="assistant", content=response))
        log_gui_model_message(model, username, " ".join(response.split()))
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

    user_message = remove_args(user_prompt)
    sys_message = get_system_message(user_prompt)

    if (
        not config.TOS_VIOLATION
        and is_violated_tos(user_message)
        and config.HOST_USERNAME != username
    ):
        gui_logger.warning(
            f"Request '{user_prompt}' by user {username} violates OPENAI TOS. Skipping..."
        )
        return

    payload = [
        sys_message,
        Message(role="assistant", content=config.GREETING),
        Message(role="user", content=user_message),
    ]

    response = get_response(payload, username, model)

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
        except openai.error.AuthenticationError:
            log_gui_general_message("Your OpenAI api key is invalid.")
            main_logger.error("OpenAI API key is invalid.")
            return
        except Exception as e:
            log_gui_general_message(f"Unhandled error happened! Cancelling ({e})")
            main_logger.error(f"Unhandled error happened! Cancelling ({e})")
            return

    if attempts == max_attempts:
        log_gui_general_message("Max number of attempts reached! Try again later!")
        main_logger(f"Max number of attempts reached. [{max_attempts}/{max_attempts}]")
