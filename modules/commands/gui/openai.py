import queue
import time

import openai

from modules.api.llm.openai import OpenAILLMProvider
from modules.logs import get_logger
from modules.typing import Message

main_logger = get_logger("main")
gui_logger = get_logger("gui")

GPT3_PROMPTS_QUEUE: queue.Queue = queue.Queue()


def handle_gpt3(command, shared_dict):
    prompt = command.removeprefix("gpt3 ").strip()
    GPT3_PROMPTS_QUEUE.put(prompt)


def gpt3_cmd_handler() -> None:
    while True:
        if GPT3_PROMPTS_QUEUE.qsize() != 0:
            prompt = GPT3_PROMPTS_QUEUE.get()
            try:
                response = OpenAILLMProvider.get_completion_text(
                    [Message(role="user", content=prompt)],
                    "admin",
                    model="gpt-3.5-turbo",
                    settings=None,
                )
                gui_logger.info(f"GPT3> {response}")
            except openai.RateLimitError:
                gui_logger.warning("Rate Limited! Try again later.")
            except Exception as e:
                main_logger.error(f"Unhandled exception from request from gui. [{e}]")
        else:
            time.sleep(2)
