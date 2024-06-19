export interface Settings {
  APP_VERSION: string;
  CONFIG_NAME: string;
  HOST_USERNAME: string;
  HOST_STEAMID3: string;
  FALLBACK_TO_USERNAME: boolean;
  GROQ_API_KEY: string

  TF2_LOGFILE_PATH: string;
  OPENAI_API_KEY: string;

  STEAM_WEBAPI_KEY: string;
  DISABLE_KEYBOARD_BINDINGS: boolean;

  CLEAR_CHAT_COMMAND: string;
  RTD_COMMAND: string;
  ENABLE_STATS_LOGS: boolean;

  RCON_HOST: string;
  RCON_PASSWORD: string;
  RCON_PORT: number;

  ENABLE_SHORTENED_USERNAMES_RESPONSE: boolean;
  SHORTENED_USERNAMES_FORMAT: string;
  SHORTENED_USERNAME_LENGTH: number;
  DELAY_BETWEEN_MESSAGES: number;

  RTD_MODE: number;

  CUSTOM_MODEL_HOST: string;
  CONFIRMABLE_QUEUE: boolean;
}
