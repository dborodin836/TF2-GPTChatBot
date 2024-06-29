from modules.logs import log_gui_general_message, main_logger


class StateManager:
    def __init__(self):
        self.bot_running = True

    def start_bot(self) -> None:
        self.bot_running = True
        main_logger.info("Bot started.")
        log_gui_general_message("BOT STARTED")

    def stop_bot(self) -> None:
        self.bot_running = False
        main_logger.info("Bot stopped.")
        log_gui_general_message("BOT STOPPED")

    def switch_state(self) -> None:
        if self.bot_running:
            self.stop_bot()
        else:
            self.start_bot()


state_manager = StateManager()
