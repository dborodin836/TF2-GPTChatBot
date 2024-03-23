export interface Settings {
    APP_VERSION: string;
    CONFIG_NAME: string;
    HOST_USERNAME: string;
    HOST_STEAMID3: string;
    TOS_VIOLATION: boolean;
    FALLBACK_TO_USERNAME: boolean;

    TF2_LOGFILE_PATH: string;
    OPENAI_API_KEY: string;

    STEAM_WEBAPI_KEY: string;
    DISABLE_KEYBOARD_BINDINGS: boolean;
    GPT4_COMMAND: string;
    GPT4_LEGACY_COMMAND: string;

    ENABLE_OPENAI_COMMANDS: boolean;
    GPT3_MODEL: string;
    GPT3_CHAT_MODEL: string;
    GPT4_MODEL: string;
    GPT4L_MODEL: string;

    GPT_COMMAND: string;
    CHATGPT_COMMAND: string;
    CLEAR_CHAT_COMMAND: string;
    RTD_COMMAND: string;
    GLOBAL_CHAT_COMMAND: string;
    GPT4_ADMIN_ONLY: boolean;
    ENABLE_STATS_LOGS: boolean;

    CUSTOM_PROMPT: string;

    RCON_HOST: string;
    RCON_PASSWORD: string;
    RCON_PORT: number;

    SOFT_COMPLETION_LIMIT: number;
    HARD_COMPLETION_LIMIT: number;
    ENABLE_SHORTENED_USERNAMES_RESPONSE: boolean;
    SHORTENED_USERNAMES_FORMAT: string;
    SHORTENED_USERNAME_LENGTH: number;
    DELAY_BETWEEN_MESSAGES: number;
    ENABLE_SOFT_LIMIT_FOR_CUSTOM_MODEL: boolean;

    RTD_MODE: number;

    ENABLE_CUSTOM_MODEL: boolean;
    CUSTOM_MODEL_HOST: string;
    CUSTOM_MODEL_COMMAND: string;
    CUSTOM_MODEL_CHAT_COMMAND: string;
    GLOBAL_CUSTOM_CHAT_COMMAND: string;
    GREETING: string;

    CONFIRMABLE_QUEUE: boolean;

    CUSTOM_MODEL_SETTINGS: string;
}