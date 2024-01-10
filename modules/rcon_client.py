from rcon.source import Client

from config import config


class RconClient(Client):
    def __init__(self, *args, **kwargs):
        super().__init__(config.RCON_HOST, config.RCON_PORT, *args, passwd=config.RCON_PASSWORD, **kwargs)
