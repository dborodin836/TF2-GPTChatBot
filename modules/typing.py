from typing import Callable, List, Literal, NamedTuple, TypedDict

from pydantic import BaseModel


class Message(TypedDict):
    role: Literal["assistant", "user", "system"]
    content: str


MessageHistory = List[Message]

BufferedMessageType = Literal["GUI", "LOG", "BOTH"]
BufferedMessageLevel = Literal["TRACE", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


class Command(NamedTuple):
    name: str
    function: Callable
    description: str


class QueuedMessage(NamedTuple):
    text: str
    is_team_chat: bool


class BufferedMessage(NamedTuple):
    type: BufferedMessageType
    level: BufferedMessageLevel
    message: str
    fail_startup: bool


class SteamHoursApiUrlID64(NamedTuple):
    url: str
    steamid64: int


class Player(BaseModel):
    name: str
    steamid3: str
    steamid64: int | None = None

    kills: int = 0
    melee_kills: int = 0
    crit_melee_kills: int = 0
    deaths: int = 0

    minutes_on_server: int
    last_updated: int
    ping_list: List[int] = []
    ping: int = 0

    @property
    def kd(self):
        if self.deaths == 0:
            kd = self.kills
        else:
            kd = round(self.kills / self.deaths, 2)
        return kd

    @property
    def melee_crit_kills_percentage(self) -> str:
        if self.melee_kills == 0:
            return "no data"

        percentage = round(self.crit_melee_kills / self.melee_kills * 100, 2)

        return f"Melee crit kill {self.crit_melee_kills}/{self.melee_kills} ({percentage}%)"


class LogLine(NamedTuple):
    """
    Represents a line from a log file.
    """

    prompt: str
    username: str
    is_team_message: bool
    player: Player
