from typing import List, Dict, NamedTuple

Message = Dict[str, str]

MessageHistory = List[Message]


class LogLine(NamedTuple):
    """
    Represents a line from a log file.
    """
    prompt: str
    username: str
    is_team_message: bool
