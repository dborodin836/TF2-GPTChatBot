from typing import Optional

from config import config
from modules.lobby_manager import lobby_manager
from modules.typing import Message, MessageHistory
from modules.utils.prompts import PROMPTS, get_prompt_by_name
from modules.utils.text import get_args, remove_args


class ConversationHistory:
    def __init__(self, settings: dict = None):
        self.custom_prompt: str = ""
        self.enable_soft_limit: bool = True
        self.enable_stats: bool = False
        self.message_history: MessageHistory = list()
        self.settings = settings or {}

    def _get_system_message(self) -> Message:
        sys_msg = []

        prompt_text = ''
        if prompt_name := self.settings.get('prompt-file'):
            prompt_text = get_prompt_by_name(prompt_name)

        if prompt := prompt_text or self.custom_prompt:
            sys_msg.append(prompt)

        # Soft limiting the response
        enable_soft_limit = self.settings.get('enable-soft-limit') if self.settings.get('enable-soft-limit') else self.enable_soft_limit
        if enable_soft_limit:
            length = self.settings.get('soft-limit-length') if self.settings.get('soft-limit-length') else config.SOFT_COMPLETION_LIMIT
            sys_msg.append(f"Answer in less than {length} chars!")

        # Add custom prompt. Acts as a prompt suffix.
        if prompt := self.settings.get('message-suffix') or config.CUSTOM_PROMPT:
            sys_msg.append(prompt)

        # Stats
        if self.enable_stats:
            sys_msg.insert(
                0, f"{lobby_manager.get_data()} Based on this data answer following question."
            )
            sys_msg.append("Ignore unknown data.")

        return Message(role="system", content=" ".join(sys_msg))

    def get_messages_array(self) -> MessageHistory:
        array = [self._get_system_message()]

        if greeting := self.settings.get('greeting') or config.GREETING:
            array.append(Message(role="assistant", content=greeting))

        array.extend(self.message_history)

        self.reset_turn()

        return array

    def add_assistant_message(self, message: Message) -> None:
        self.message_history.append(message)

    def add_user_message_from_prompt(
            self, user_prompt: str, enable_soft_limit: bool = True
    ) -> None:
        user_message = remove_args(user_prompt)
        args = get_args(user_prompt)

        if self.settings.get('allow-prompt-overwrite', True):
            for prompt in PROMPTS:
                if prompt["flag"] in args:
                    self.custom_prompt = prompt["prompt"]
                    break
        if self.settings.get('allow-long', True):
            if r"\l" in args or not enable_soft_limit or self.settings.get('allow-long', True):
                self.enable_soft_limit = False

        if r"\stats" in args:
            self.enable_stats = True

        self.message_history.append(Message(role="user", content=user_message))

    def reset_turn(self):
        self.enable_soft_limit = True
        self.enable_stats = False

    def reset(self):
        self.custom_prompt = ""
        self.enable_soft_limit = True
        self.message_history = list()
