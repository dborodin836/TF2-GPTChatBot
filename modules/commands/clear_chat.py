from modules.typing import LogLine


def handle_clear(logline: LogLine, shared_dict: dict):
    shared_dict["CHAT_CONVERSATION_HISTORY"].reset()