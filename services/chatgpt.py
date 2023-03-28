import openai
import hashlib
from config import OPENAI_API_KEY


def send_gpt_completion_request(message: str, username: str) -> str:
    openai.api_key = OPENAI_API_KEY

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": message}],
        user=hashlib.md5(username.encode()).hexdigest()
    )

    response_text = completion.choices[0].message["content"].strip()
    return response_text
