import io
from typing import Optional

import pygame

from modules.api.llm.openai import get_tts
from modules.command_controllers import InitializerConfig
from modules.commands.base import BaseCommand
from modules.typing import LogLine
from modules.utils.text import remove_args


class TTSCommand(BaseCommand):
    @classmethod
    def get_handler(cls):
        def func(logline: LogLine, shared_dict: InitializerConfig) -> Optional[str]:
            msg = remove_args(logline.prompt)
            result = get_tts(msg, cls.settings)

            pygame.mixer.init(devicename=cls.settings.get("output_device", None))
            sound = pygame.mixer.Sound(io.BytesIO(result.content))
            sound.set_volume(cls.settings.get('volume', 1.0))
            sound.play()
            # Keep the program running until the sound has finished playing
            while pygame.mixer.get_busy():
                pygame.time.Clock().tick(10)

            return 'OK' if result.response.status_code == 200 else 'ERROR'

        return func
