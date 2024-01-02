import re
import time

import openai
import hashlib
from config import config
from services.source_game import send_say_command_to_tf2
from utils.logs import log_message, log_cmd_message, log_to_file
from utils.text import add_prompts_by_flags
from utils.types import MessageHistory


def is_violated_tos(message: str) -> bool:
    openai.api_key = config.OPENAI_API_KEY
    try:
        response = openai.Moderation.create(
            input=message,
        )
    except openai.error.APIError:
        return False

    return response.results[0]['flagged']


def send_gpt_completion_request(conversation_history: MessageHistory, username: str, model: str) -> str:
    openai.api_key = config.OPENAI_API_KEY

    completion = openai.ChatCompletion.create(
        model=model,
        messages=conversation_history,
        user=hashlib.md5(username.encode()).hexdigest()
    )

    response_text = completion.choices[0].message["content"].strip()
    return response_text


def handle_cgpt_request(username: str, user_prompt: str, conversation_history: MessageHistory,
                        model, is_team: bool = False) -> MessageHistory:
    """
    This function is called when the user wants to send a message to the AI chatbot. It logs the
    user's message, and sends a request to GPT-3 to generate a response. Finally, the function
    sends the generated response to the TF2 game.
    """
    log_message(model.upper(), username, user_prompt)

    message = add_prompts_by_flags(user_prompt)

    if not config.TOS_VIOLATION and is_violated_tos(message) and config.HOST_USERNAME != username:
        print(f"Request '{user_prompt}' violates OPENAI TOS. Skipping...")
        return MessageHistory

    conversation_history.append({"role": "user", "content": message})

    response = get_response(conversation_history, username, model)

    if response:
        conversation_history.append({"role": "assistant", "content": response})
        log_message(model.upper(), username, ' '.join(response.split()))
        send_say_command_to_tf2(response, is_team)

    return conversation_history


def handle_gpt_request(username: str, user_prompt: str, model: str, is_team: bool = False) -> None:
    """
    This function is called when the user wants to send a message to the AI chatbot. It logs the
    user's message, and sends a request to GPT-3 to generate a response. Finally, the function
    sends the generated response to the TF2 game.
    """
    log_message("GPT3", username, user_prompt)

    message = add_prompts_by_flags(user_prompt)

    if not config.TOS_VIOLATION and is_violated_tos(message) and config.HOST_USERNAME != username:
        print(f"Request '{user_prompt}' violates OPENAI TOS. Skipping...")
        return

    response = get_response([{"role": "user", "content": message}], username, model)

    if response:
        log_message("GPT3", username, ' '.join(response.split()))
        send_say_command_to_tf2(response, is_team)


def get_response(conversation_history: MessageHistory, username: str, model) -> str | None:
    attempts = 0
    max_attempts = 2

    while attempts < max_attempts:
        try:
            response = send_gpt_completion_request(conversation_history, username, model=model)
            filtered_response = remove_hashtags(response)
            return filtered_response
        except openai.error.RateLimitError:
            log_cmd_message("Rate limited! Trying again...")
            time.sleep(2)
            attempts += 1
        except openai.error.APIError as e:
            log_cmd_message(f"Wasn't able to connect to OpenAI API. Cancelling...")
            log_to_file(str(e))
            return
        except Exception as e:
            log_cmd_message(f"Unhandled error happened! Trying again... ({e})")
            return

    if attempts == max_attempts:
        log_cmd_message("Max number of attempts reached! Try again later!")


def remove_hashtags(text: str) -> str:
    """
    Removes hashtags from a given string.
    """
    cleaned_text = re.sub(r'#\w+', '', text).strip()
    return cleaned_text
