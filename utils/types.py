from typing import List, Literal, NamedTuple, TypedDict

from pydantic import BaseModel


class Message(TypedDict):
    role: Literal["assistant", "user", "system"]
    content: str


MessageHistory = List[Message]


class SteamHoursApiUrlID64(NamedTuple):
    url: str
    steamid64: int


class LogLine(NamedTuple):
    """
    Represents a line from a log file.
    """
    prompt: str
    username: str
    is_team_message: bool


class Player(BaseModel):
    name: str
    steamid3: str
    steamid64: int | None = None

    kills: int = 0
    deaths: int = 0

    minutes_on_server: int
    last_updated: int
    ping_list: List[int] = []
    ping: int = 0
