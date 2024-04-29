import hashlib
import time

import openai

from config import config
from modules.api.base import LLMProvider
from modules.logs import get_logger, log_gui_general_message, log_gui_model_message
from modules.servers.tf2 import send_say_command_to_tf2
from modules.typing import Message
from modules.utils.text import get_system_message, remove_args, remove_hashtags

main_logger = get_logger("main")
gui_logger = get_logger("gui")


class OpenAILLMProvider(LLMProvider):

    @staticmethod
    def _get_provider_response(conversation_history, username, model):
        openai.api_key = config.OPENAI_API_KEY

        completion = openai.ChatCompletion.create(
            model=model,
            messages=conversation_history,
            user=hashlib.md5(username.encode()).hexdigest(),
        )

        response_text = completion.choices[0].message["content"].strip()
        return response_text

    @staticmethod
    def _try_get_response(conversation_history, username, model):
        attempts = 0
        max_attempts = 2

        while attempts < max_attempts:
            try:
                response = OpenAILLMProvider._get_provider_response(conversation_history, username, model=model)
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
