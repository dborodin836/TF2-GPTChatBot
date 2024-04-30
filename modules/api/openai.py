import hashlib

import openai

from config import config
from modules.api.base import LLMProvider
from modules.logs import get_logger

main_logger = get_logger("main")
gui_logger = get_logger("gui")


class OpenAILLMProvider(LLMProvider):

    @staticmethod
    def get_completion_text(conversation_history, username, model, settings):
        openai.api_key = config.OPENAI_API_KEY

        if isinstance(settings, dict):
            completion = openai.ChatCompletion.create(
                model=model,
                messages=conversation_history,
                user=hashlib.md5(username.encode()).hexdigest(),
                **settings
            )
        else:
            completion = openai.ChatCompletion.create(
                model=model,
                messages=conversation_history,
                user=hashlib.md5(username.encode()).hexdigest(),
            )

        response_text = completion.choices[0].message["content"].strip()
        return response_text


def is_flagged(message: str) -> bool:
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
