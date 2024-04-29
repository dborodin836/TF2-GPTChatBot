import hashlib
import time

import groq

from config import config
from modules.api.base import LLMProvider
from modules.logs import get_logger, log_gui_general_message, log_gui_model_message
from modules.servers.tf2 import send_say_command_to_tf2
from modules.typing import Message
from modules.utils.text import get_system_message, remove_args, remove_hashtags

main_logger = get_logger("main")
gui_logger = get_logger("gui")


class GroqCloudLLMProvider(LLMProvider):

    @staticmethod
    def get_quick_query_completion(username, user_prompt, model, is_team_chat=False):
        log_gui_model_message(model, username, user_prompt)

        user_message = remove_args(user_prompt)
        sys_message = get_system_message(user_prompt)

        payload = [
            sys_message,
            Message(role="assistant", content=config.GREETING),
            Message(role="user", content=user_message),
        ]

        response = GroqCloudLLMProvider._try_get_response(payload, username, model)

        if response:
            log_gui_model_message(model, username, " ".join(response.split()))
            send_say_command_to_tf2(response, username, is_team_chat)

    @staticmethod
    def get_chat_completion(username, user_prompt, conversation_history, model, is_team=False):
        log_gui_model_message(model, username, user_prompt)

        user_message = remove_args(user_prompt)

        conversation_history.add_user_message_from_prompt(user_message)

        response = GroqCloudLLMProvider._try_get_response(conversation_history.get_messages_array(), username, model)

        if response:
            conversation_history.add_assistant_message(Message(role="assistant", content=response))
            log_gui_model_message(model, username, " ".join(response.split()))
            send_say_command_to_tf2(response, username, is_team)

        return conversation_history

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
