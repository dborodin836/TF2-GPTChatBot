from config import *
from services.network import check_connection
from utils.chat import handle_gpt_request
from utils.logs import log_message
from utils.prompt import load_prompts
from utils.text import open_tf2_logfile


def main() -> None:
    # Initialize conversation history
    conversation_history = ''

    check_connection()

    # Load prompts from .xtx files
    load_prompts()
    print("Ready to use!")


    # Loop through log file
    for line, user in open_tf2_logfile():
        # Handle GPT3 completion requests
        if line.strip().startswith(GPT_COMMAND):
            prompt = line.removeprefix(GPT_COMMAND).strip()
            conversation_history = handle_gpt_request("GPT3", user, prompt, conversation_history)

        # Handle ChatGPT requests
        if line.strip().startswith(CHATGPT_COMMAND):
            prompt = line.removeprefix(CHATGPT_COMMAND).strip()
            conversation_history = handle_gpt_request("CHAT", user, prompt, conversation_history)

        # Handle clear chat requests
        if line.strip().startswith(CLEAR_CHAT_COMMAND):
            log_message("CHAT", user, "CLEARING CHAT")
            conversation_history = ''


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print()

