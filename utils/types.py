from typing import List, Dict, NamedTuple

from pydantic import BaseModel

Message = Dict[str, str]

MessageHistory = List[Message]


class LogLine(NamedTuple):
    """
    Represents a line from a log file.
    """
    prompt: str
    username: str
    is_team_message: bool


class Player(BaseModel):
    name: str

    kills: int = 0
    deaths: int = 0

    minutes_on_server: int
    last_updated: int
