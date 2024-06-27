import queue
import time
from typing import Optional

from config import config
from modules.command_controllers import InitializerConfig
from modules.logs import get_logger
from modules.rcon_client import RconClient
from modules.typing import GameChatMessage, QueuedMessage
from modules.utils.text import has_cyrillic

message_queue: queue.Queue = queue.Queue()

main_logger = get_logger("main")
gui_logger = get_logger("gui")
combo_logger = get_logger("combo")


class ConfirmableQueueManager:
    queue: queue.Queue
    is_locked: bool = False
    awaited_message: Optional[str] = None
    last_confirmed_message: float
    warning_sent = False

    def __init__(self, q):
        self.queue = q

    def clean(self) -> None:
        """
        Method to clean the queue and reset flags.
        """
        self.queue = queue.Queue()
        self.is_locked = False
        self.awaited_message = None
        self.last_confirmed_message = time.time()
        self.warning_sent = False

    def start_worker(self) -> None:
        """
        Worker method to handle messages in the queue.
        """
        while True:
            queued_message: QueuedMessage = self.queue.queue[0]

            if self.is_locked:
                # Check for queue activity and handle timeouts
                # Send gui messages based on time intervals
                time.sleep(0.5)
                if time.time() - self.last_confirmed_message > 30:
                    combo_logger.debug("Queue seems to be dead. Cleaning...")
                    self.clean()
                elif time.time() - self.last_confirmed_message > 15:
                    send_say_cmd(queued_message)
                elif time.time() - self.last_confirmed_message > 10:
                    if not self.warning_sent:
                        combo_logger.debug("You're likely to be muted by tf2.")
                        self.warning_sent = True
                continue

            if not self.queue.empty():
                # Process queued messages
                # Lock the queue, send message, and update flags
                if has_cyrillic(queued_message.text):
                    # In case message gets stripped in chat.
                    self.awaited_message = queued_message.text[: len(queued_message.text) // 2]
                else:
                    self.awaited_message = queued_message.text
                self.is_locked = True
                main_logger.trace("Locking queue")
                self.last_confirmed_message = time.time()
                send_say_cmd(queued_message)
            else:
                time.sleep(0.5)

    def unlock_queue(self) -> None:
        """
        Unlock the queue, remove processed message, and reset flags.
        """
        main_logger.trace("Unlocking queue")
        self.queue.get()
        self.awaited_message = None
        self.is_locked = False
        self.warning_sent = False
        self.last_confirmed_message = time.time()

    def get_awaited_msg(self) -> Optional[str]:
        """
        Return the awaited message if present, else None.
        """
        if self.awaited_message is not None:
            main_logger.trace(f"Requested awaited message '{self.awaited_message}'")
        return self.awaited_message


def send_say_cmd(queued_message: QueuedMessage) -> None:
    """
    Construct and send the appropriate say command.
    """
    if queued_message.is_team_chat:
        cmd = f'say_team "{queued_message.text}";'
    else:
        cmd = f'say "{queued_message.text}";'

    with RconClient() as client:
        try:
            main_logger.debug(f"Sending command [{cmd}]")
            client.run(cmd)
        except Exception as e:
            main_logger.error(f"Unhandled exception happened. [{e}]")
    time.sleep(config.DELAY_BETWEEN_MESSAGES)


def message_queue_handler() -> None:
    """
    Check if using confirmable queue. Process messages from either regular or confirmable queue.
    """
    if not config.CONFIRMABLE_QUEUE:
        while True:
            if not message_queue.empty():
                queued_message: QueuedMessage = message_queue.get()
                main_logger.trace(f"Retrieved message '{queued_message.text}' from queue")

                send_say_cmd(queued_message)
            else:
                time.sleep(0.5)
    else:
        confirmable_queue_manager.start_worker()


def messaging_queue_service(logline: GameChatMessage, shared_dict: InitializerConfig):
    """
    Check for awaited message and unlock the queue if found.
    """
    awaited_msg = confirmable_queue_manager.get_awaited_msg()
    if awaited_msg is not None and awaited_msg in logline.prompt:
        confirmable_queue_manager.unlock_queue()


confirmable_queue_manager = ConfirmableQueueManager(message_queue)
