from typing import Optional

from modules.command_controllers import InitializerConfig
from modules.commands.base import BaseCommand
from modules.logs import get_logger
from modules.rcon_client import RconClient
from modules.typing import LogLine


class RconCommand(BaseCommand):
    command: str

    @classmethod
    def get_handler(cls):
        def func(logline: LogLine, shared_dict: InitializerConfig) -> Optional[str]:
            if logline.prompt.strip():
                cmd = (
                    f"wait {cls.settings.get('wait-ms', 0)};{cls.command} {logline.prompt.strip()};"
                )
            else:
                cmd = f"wait {cls.settings.get('wait-ms', 0)};{cls.command};"
            with RconClient() as client:
                get_logger("gui").warning(cmd)
                client.run(cmd)
                return cmd

        return func
