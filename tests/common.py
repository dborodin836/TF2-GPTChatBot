def raise_(ex):
    raise ex


class MockConfig:
    APP_VERSION = "1.0.0"
    SOFT_COMPLETION_LIMIT = 128
    CUSTOM_PROMPT = ""
    GREETING = ""

    def __init__(
            self,
            app_version=None,
            soft_completion_limit=None,
            custom_prompt = None
    ):
        if app_version is not None:
            self.APP_VERSION = app_version
        if soft_completion_limit is not None:
            self.SOFT_COMPLETION_LIMIT = soft_completion_limit
        if custom_prompt is not None:
            self.CUSTOM_PROMPT = custom_prompt
