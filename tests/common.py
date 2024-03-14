def raise_(ex):
    raise ex


class MockConfig:
    APP_VERSION = "1.0.0"
    SOFT_COMPLETION_LIMIT = 128
    CUSTOM_PROMPT = ""
    GREETING = ""
    HOST_USERNAME = "admin"
    CLEAR_CHAT_COMMAND = "!clear"

    def __init__(
            self,
            app_version=None,
            soft_completion_limit=None,
            custom_prompt=None,
            host_username=None,
            clear_chat_command=None
    ):
        if app_version is not None:
            self.APP_VERSION = app_version
        if soft_completion_limit is not None:
            self.SOFT_COMPLETION_LIMIT = soft_completion_limit
        if custom_prompt is not None:
            self.CUSTOM_PROMPT = custom_prompt
        if host_username is not None:
            self.HOST_USERNAME = host_username
        if clear_chat_command is not None:
            self.CLEAR_CHAT_COMMAND = clear_chat_command
