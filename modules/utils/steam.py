import platform
from os.path import expanduser

import vdf

try:
    import winreg
except ModuleNotFoundError:
    pass

from typing import Optional

from config import config
from modules.logs import combo_logger, main_logger

STEAMID3_TO_STEAMID64_COEFFICIENT = 76561197960265728
LINUX_STEAM_LOGINUSERS = f"{expanduser('~')}/.steam/steam/config/loginusers.vdf"


def set_host_steamid3() -> None:
    steamid = get_host_steamid3()
    if steamid is not None:
        config.HOST_STEAMID3 = steamid
    else:
        combo_logger.warning("Failed to get host steamid.")


def get_host_steamid3() -> Optional[str]:
    if platform.system() == "Windows":
        return get_host_steamid3_windows()
    elif platform.system() == "Linux":
        return get_host_steamid3_linux()
    else:
        combo_logger.error("Failed to get system.")
        return None


def get_host_steamid3_windows():
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


def get_host_steamid3_linux():
    try:
        with open(LINUX_STEAM_LOGINUSERS, "r") as file:
            loginusers = vdf.load(file)
            for steamid64, user_data in loginusers.get("users", {}).items():
                if user_data.get("MostRecent", 0) == "1":
                    return steamid64_to_steamid3(steamid64)

            return None
    except Exception as e:
        combo_logger.error(f"Failed to get host steamid3 [{e}]")
        return None


def steamid64_to_steamid3(steamid64: int) -> str:
    steamid3 = []
    steamid3.append("[U:1:")
    account_id = int(steamid64) - STEAMID3_TO_STEAMID64_COEFFICIENT

    steamid3.append(str(account_id) + "]")

    return "".join(steamid3)


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
