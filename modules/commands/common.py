from modules.types import LogLine


def handle_clear(logline: LogLine, **kwargs):
    kwargs.update({"CHAT_CONVERSATION_HISTORY": []})
    return kwargs
