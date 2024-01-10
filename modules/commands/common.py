from modules.types import LogLine


def handle_clear(logline: LogLine, shared_dict: dict):
    shared_dict.update({"CHAT_CONVERSATION_HISTORY": []})
