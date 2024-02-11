from config import config
from modules.tf_statistics import StatsData
from modules.typing import MessageHistory, Message
from modules.utils.prompts import PROMPTS
from modules.utils.text import remove_args, get_args


class ConversationHistory:
    custom_prompt: str = ""
    enable_soft_limit: bool = True
    enable_stats: bool = False
    message_history: MessageHistory = list()

    def _get_system_message(self) -> Message:
        sys_msg = []

        if self.custom_prompt:
            sys_msg.append(self.custom_prompt)

        if self.enable_soft_limit:
            sys_msg.append(f"Answer in less than {config.SOFT_COMPLETION_LIMIT} chars!")

        if config.CUSTOM_PROMPT:
            sys_msg.append(config.CUSTOM_PROMPT)

        if self.enable_stats:
            sys_msg.insert(0, f"{StatsData.get_data()} Based on this data answer following question.")
            sys_msg.append("Ignore unknown data.")

        return Message(role="system", content=" ".join(sys_msg))

    def get_messages_array(self) -> MessageHistory:
        array = [self._get_system_message()]
        array.extend(self.message_history)

        # Reset
        self.enable_soft_limit = True
        self.enable_stats = False

        import pprint
        pprint.pprint(array)

        return array

    def add_assistant_message(self, message: Message) -> None:
        self.message_history.append(message)

    def add_user_message_from_prompt(self, user_prompt: str, enable_soft_limit: bool = True) -> None:
        user_message = remove_args(user_prompt)
        args = get_args(user_prompt)

        for prompt in PROMPTS:
            if prompt["flag"] in args:
                self.custom_prompt = prompt["prompt"]
                break

        if r"\l" in args or not enable_soft_limit:
            self.enable_soft_limit = False

        if r"\stats" in args and config.ENABLE_STATS:
            self.enable_stats = True

        self.message_history.append(Message(role="user", content=user_message))

    def reset(self):
        self.custom_prompt = ""
        self.enable_soft_limit = True
        self.message_history = list()
