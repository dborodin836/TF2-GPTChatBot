import hashlib

import openai
from openai import NotGiven, OpenAI

from config import config
from modules.api.llm.base import LLMProvider
from modules.logs import get_logger

main_logger = get_logger("main")
gui_logger = get_logger("gui")


class OpenAILLMProvider(LLMProvider):

    @staticmethod
    def get_completion_text(conversation_history, username, model, settings):
        client = OpenAI(
            api_key=config.OPENAI_API_KEY,
        )

        if isinstance(settings, dict):
            completion = client.chat.completions.create(
                model=model,
                messages=conversation_history,
                user=hashlib.md5(username.encode()).hexdigest(),
                **settings,
            )
        else:
            completion = client.chat.completions.create(
                model=model,
                messages=conversation_history,
                user=hashlib.md5(username.encode()).hexdigest(),
            )

        response_text = completion.choices[0].message.content.strip()
        return response_text


def is_flagged(message: str) -> bool:
    client = OpenAI(api_key=config.OPENAI_API_KEY)
    try:
        response = client.moderations.create(
            input=message,
        )
    except openai.APIError:
        main_logger.error("Failed to moderate message. [APIError]")
        return True
    except Exception as e:
        main_logger.error(f"Failed to moderate message. [{e}]")
        return True

    return response.results[0].flagged


def get_tts(message: str, settings: dict):
    client = OpenAI(
        api_key=config.OPENAI_API_KEY,
    )

    response = client.audio.speech.create(
        model=settings.get("model", "tts-1"),
        voice=settings.get("voice", "alloy"),
        input=message,
        speed=settings.get("speed", NotGiven()),
    )

    return response
