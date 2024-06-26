import hashlib

import groq

from config import config
from modules.api.llm.base import LLMProvider
from modules.utils.text import remove_hashtags


class GroqCloudLLMProvider(LLMProvider):

    @staticmethod
    def get_completion_text(message_array, username, model, settings):
        client = groq.Groq(max_retries=0, api_key=config.GROQ_API_KEY)

        if isinstance(settings, dict):
            completion = client.chat.completions.create(
                model=model,
                messages=message_array,
                user=hashlib.md5(username.encode()).hexdigest(),
                **settings
            )
        else:
            completion = client.chat.completions.create(
                model=model,
                messages=message_array,
                user=hashlib.md5(username.encode()).hexdigest(),
            )

        response_text = completion.choices[0].message.content.strip()
        filtered_response = remove_hashtags(response_text)
        return filtered_response
