from typing import List, Dict, NamedTuple

MessageHistory = List[Dict[str, str]]


class LogLine(NamedTuple):
    """
    Represents a line from a log file.
    """
    prompt: str
    username: str
    is_team_message: bool
