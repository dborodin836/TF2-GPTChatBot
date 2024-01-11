STEAMID3_TO_STEAMID64_COEFFICIENT = 76561197960265728


def steamid3_to_steamid64(steamid3: str) -> int:
    """
    This function converts a SteamID3 ([U:X:XXXXXXX]) string to a SteamID64 (XXXXXXXXXXXXXXXXX) integer and returns it.
    It removes any square bracket characters, extracts the numerical identifier, calculates the SteamID64 by adding
    a pre-defined constant, and returns it.
    """
    for ch in ["[", "]"]:
        if ch in steamid3:
            steamid3 = steamid3.replace(ch, "")

    steamid3_split = steamid3.split(":")
    steamid64 = int(steamid3_split[2]) + STEAMID3_TO_STEAMID64_COEFFICIENT

    return steamid64
