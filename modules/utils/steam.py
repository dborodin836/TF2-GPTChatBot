try:
    import winreg
except ModuleNotFoundError:
    pass

from typing import Optional

from config import config
from modules.logs import get_logger

main_logger = get_logger("main")
combo_logger = get_logger("combo")


STEAMID3_TO_STEAMID64_COEFFICIENT = 76561197960265728


def set_host_steamid3() -> None:
    steamid = get_host_steamid3()
    if steamid is not None:
        config.HOST_STEAMID3 = steamid
    else:
        combo_logger.warning("Failed to get host steamid.")


# TODO: This is, obviously, windows specific.
def get_host_steamid3() -> Optional[str]:
    key_path = r"Software\Valve\Steam\ActiveProcess"

    # Open the registry key
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path)
        value, _ = winreg.QueryValueEx(key, "ActiveUser")
        winreg.CloseKey(key)
        return f"[U:1:{value}]"
    except Exception as e:
        main_logger.error(f"Failed to get host steamid3 [{e}]")
        return None


def steamid3_to_steamid64(steamid3: str) -> int:
    """
    This function converts a SteamID3 ([U:X:XXXXXXX]) string to a SteamID64 (XXXXXXXXXXXXXXXXX) integer and returns it.
    It removes any square bracket characters, extracts the numerical identifier, calculates the SteamID64 by adding
    a pre-defined constant, and returns it.

    https://developer.valvesoftware.com/wiki/SteamID
    """
    for ch in ["[", "]"]:
        if ch in steamid3:
            steamid3 = steamid3.replace(ch, "")

    steamid3_split = steamid3.split(":")
    steamid64 = int(steamid3_split[2]) + STEAMID3_TO_STEAMID64_COEFFICIENT

    return steamid64
