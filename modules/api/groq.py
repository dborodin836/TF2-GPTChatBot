import hashlib
import time

import groq

from config import config
from modules.api.base import LLMProvider
from modules.logs import get_logger, log_gui_general_message
from modules.utils.text import remove_hashtags

main_logger = get_logger("main")
gui_logger = get_logger("gui")


class GroqCloudLLMProvider(LLMProvider):

    @staticmethod
    def _get_provider_response(conversation_history, username, model):
        client = groq.Groq(
            max_retries=0,
            api_key=config.GROQ_API_KEY
        )

        completion = client.chat.completions.create(
            model=model,
            messages=conversation_history,
            user=hashlib.md5(username.encode()).hexdigest(),
        )

        response_text = completion.choices[0].message.content.strip()
        return response_text

    @staticmethod
    def _try_get_response(conversation_history, username, model):
        attempts = 0
        max_attempts = 2

        while attempts < max_attempts:
            try:
                response = GroqCloudLLMProvider._get_provider_response(conversation_history, username, model=model)
                filtered_response = remove_hashtags(response)
                return filtered_response
            except groq.RateLimitError:
                log_gui_general_message("Rate limited! Trying again...")
                main_logger(f"User is rate limited.")
                time.sleep(2)
                attempts += 1
            except groq.APIError as e:
                log_gui_general_message(f"Wasn't able to connect to Groq API. Cancelling...")
                main_logger.error(f"APIError happened. [{e}]")
                return
            except groq.AuthenticationError:
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
