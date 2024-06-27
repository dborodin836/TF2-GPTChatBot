import enum
from typing import (
    Callable,
    Dict,
    List,
    Literal,
    NamedTuple,
    Optional,
    Set,
    Type,
    TypedDict,
    Union,
)

from pydantic import BaseModel


class Message(TypedDict):
    role: Literal["assistant", "user", "system"]
    content: Union[str, List[Dict[Literal["text", "image_url"], Union[str, Dict[str, str]]]]]


MessageHistory = List[Message]

BufferedMessageType = Literal["GUI", "LOG", "BOTH"]
BufferedMessageLevel = Literal["TRACE", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


class GuiCommand(NamedTuple):
    name: str
    function: Callable
    description: str


class CommandSchemaDefinition(NamedTuple):
    klass: Type
    loader: Type
    settings: Set[str] = set()


class Command(NamedTuple):
    full_name: str
    ref_name: Optional[str]
    # Callable[[LogLine, InitializerConfig], Optional[str]
    function: Callable
    meta: Optional[Dict]


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


class VACStats(BaseModel):
    is_VAC_banned: str
    number_of_bans: str
    days_since_last_ban: str


class PlayerSteamInfo(BaseModel):
    steamid64: int
    steam_account_age: str
    hours_in_team_fortress_2: str
    country: str
    real_name: str
    VAC: Optional[VACStats]


class PlayerStats(BaseModel):
    name: str
    steam: PlayerSteamInfo
    deaths: int
    kills: int
    melee_crit_percentage: str
    kill_death_ratio: float
    avg_ping: int
    minutes_on_server: int


class Player(BaseModel):
    name: str
    steamid3: str
    steamid64: int

    kills: int = 0
    melee_kills: int = 0
    crit_melee_kills: int = 0
    deaths: int = 0

    minutes_on_server: int
    last_updated: float
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


class GameChatMessage(NamedTuple):
    """
    Represents a chat message parsed from a log file.
    """
    prompt: str
    username: str
    is_team_message: bool
    player: Player


class ConfirmationStatus(enum.Enum):
    CONFIRMED = 1
    WAITING = 2
