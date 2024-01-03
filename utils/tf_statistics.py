import datetime
import time
from statistics import mean
from typing import List

import requests

from config import config
from utils.bulk_url_downloader import BulkSteamGameDetailsUrlDownloader
from utils.logs import get_logger
from utils.types import Player, SteamHoursApiUrlID64

STEAMID3_TO_STEAMID64_COEEFICIENT = 76561197960265728

main_logger = get_logger("main")
gui_logger = get_logger("gui")
combo_logger = get_logger("combo")

MELEE_WEAPONS_KILL_IDS = {
    "skullbat",
    "nonnonviolent_protest",
    "crossing_guard",
    "disciplinary_action",
    "memory_maker",
    "unique_pickaxe",
    "unique_pickaxe_escape",
    "freedom_staff",
    "fryingpan",
    "market_gardener",
    "golden_fryingpan",
    "demokatana",
    "ham_shank",
    "necro_smasher",
    "paintrain",
    "sandman",
    "saxxy",
    "shovel",
    "bat",
    "boston_basher",
    "candy_cane",
    "holymackerel",
    "back_scratcher",
    "lava_bat",
    "scout_sword",
    "unarmed_combat",
    "wrap_assassin",
    "axtinguisher",
    "warfan",
    "fireaxe",
    "sledgehammer",
    "lollichop",
    "the_maul",
    "annihilator",
    "mailbox",
    "powerjack",
    "lava_axe",
    "thirddegree",
    "bottle",
    "claidheamohmor",
    "sword",
    "headtaker",
    "nessieclub",
    "persian_persuader",
    "batteaxe",
    "scotland_shard",
    "voodoo_pin",
    "eternal_reward" "apocofists",
    "bread_bite",
    "eviction_notice",
    "gloves_running_urgently",
    "ullapool_caber",
    "fists",
    "steel_fists",
    "holiday_punch",
    "gloves",
    "warrior_spirit",
    "eureka_effect",
    "wrench_golden",
    "robot_arm",
    "wrench_jag",
    "southern_hospitality",
    "wrench",
    "amputator",
    "bonesaw",
    "ubersaw",
    "solemn_vow",
    "battleneedle",
    "bushwacka",
    "club",
    "shahanshah",
    "tribalkukri",
    "big_earner",
    "black_rose",
    "kunai",
    "knife",
    "sharp_dresser",
    "spy_cicle",
}


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
    steamid64 = int(steamid3_split[2]) + STEAMID3_TO_STEAMID64_COEEFICIENT

    return steamid64


def get_date(epoch: int, relative_epoch_time: int = None) -> str:
    account_created_date = datetime.date.fromtimestamp(epoch)

    if relative_epoch_time is not None:
        current_date = datetime.date.fromtimestamp(relative_epoch_time)
    else:
        current_date = datetime.date.today()

    age_months = (
        current_date.month
        - account_created_date.month
        - (current_date.day < account_created_date.day)
    )
    if age_months < 0:
        age_months += 12
    age_days = (current_date - account_created_date.replace(year=current_date.year)).days
    # Get the age tuple in years, months, and days
    age = datetime.timedelta(days=age_days)
    age_years, remainder_days = divmod(age.days, 365)
    age_months, remainder_days = divmod(remainder_days, 30)
    age_days = remainder_days
    age_years = (
        current_date.year
        - account_created_date.year
        - (
            (current_date.month, current_date.day)
            < (account_created_date.month, account_created_date.day)
        )
    )
    return f"{age_years} years {age_months} months {age_days} days"


class StatsData:
    players: List[Player] = []
    map_name: str | None = None
    server_ip: str | None = None

    @classmethod
    def set_map_name(cls, map_name: str) -> None:
        cls.map_name = map_name
        combo_logger.info(f"MAP CHANGE DETECTED {map_name}")
        cls._reset_players()

    @classmethod
    def set_server_ip(cls, ip: str) -> None:
        cls.server_ip = ip

    @classmethod
    def _reset_players(cls) -> None:
        cls.players = []
        combo_logger.info("RESET PLAYERS")

    @classmethod
    def add_player(cls, new_player: Player):
        for player in cls.players:
            # If player already exist
            if player.name == new_player.name:
                # Update minutes on server and last_updated
                player.minutes_on_server = new_player.minutes_on_server
                player.last_updated = time.time()

                # Update ping
                player.ping_list.append(new_player.ping)
                player.ping = round(mean(player.ping_list))

                main_logger.trace(f"Updated players time on server {player.name}")
                return

        new_player.steamid64 = steamid3_to_steamid64(new_player.steamid3)
        cls.players.append(new_player)
        main_logger.debug(
            f"Added new player {new_player.name} with {new_player.minutes_on_server} minutes on server"
        )

    @classmethod
    def process_kill(
        cls, killer_username: str, victim_username: str, weapon: str, is_crit: bool
    ) -> None:
        main_logger.debug(
            f"'{killer_username}' killed '{victim_username} with {weapon} {'crit' if is_crit else ''}'"
        )

        for player in cls.players:
            if player.name == killer_username:
                if weapon in MELEE_WEAPONS_KILL_IDS:
                    player.melee_kills += 1
                    if is_crit:
                        player.crit_melee_kills += 1

                player.kills += 1
                main_logger.trace(
                    f"Incremented kills for a player {player.name}, current value {player.kills}"
                )
            elif player.name == victim_username:
                player.deaths += 1
                main_logger.trace(
                    f"Incremented deaths for a player {player.name}, current value {player.deaths}"
                )

    @classmethod
    def process_kill_bind(cls, username: str) -> None:
        main_logger.debug(f"{username} suicided")
        for player in cls.players:
            if player.name == username:
                player.deaths += 1
                main_logger.trace(
                    f"Incremented deaths for a player {player.name}, current value {player.deaths}"
                )

    @classmethod
    def _get_steam_profiles_data(cls, steamids64) -> List[dict]:
        try:
            response = requests.get(
                f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={config.STEAM_WEBAPI_KEY}&steamids={','.join(steamids64)}"
            ).json()
            return response["response"]["players"]
        except Exception as e:
            main_logger.warning(f"Failed to fetch steam profiles data [{e}]")
            return []

    @classmethod
    def _get_steam_ban_data(cls, steamids64) -> List[dict]:
        try:
            response = requests.get(
                f" http://api.steampowered.com/ISteamUser/GetPlayerBans/v1/?key={config.STEAM_WEBAPI_KEY}&steamids={','.join(steamids64)}"
            ).json()
            return response["players"]
        except Exception as e:
            main_logger.warning(f"Failed to fetch steam bans data [{e}]")
            return []

    @classmethod
    def get_data(cls) -> dict:
        new_players: List = []

        # Filter players, exclude those who disconnected
        cls.players = [
            player for player in cls.players if time.time() - int(player.last_updated) < 120
        ]
        id64 = [str(player.steamid64) for player in cls.players if player.steamid64 is not None]
        steam_profiles_data_list = cls._get_steam_profiles_data(id64)
        steam_bans_data = cls._get_steam_ban_data(id64)

        for player in cls.players:
            for player_steam_data in steam_profiles_data_list:
                if str(player.steamid64) == player_steam_data.get("steamid"):
                    try:
                        account_age = get_date(int(player_steam_data["timecreated"]))
                    except KeyError:
                        account_age = "unknown"

                    country = player_steam_data.get("loccountrycode", "unknown")
                    real_name = player_steam_data.get("realname", "")

                    new_players.append(
                        {
                            "name": player.name,
                            "steam": {
                                "steamid64": player.steamid64,
                                "steam_account_age": account_age,
                                "hours_in_team_fortress_2": "unknown",
                                "country": country,
                                "real_name": real_name,
                            },
                            "deaths": player.deaths,
                            "kills": player.kills,
                            "melee_crit_percentage": cls._get_melee_kill_percentage(player),
                            "k/d": cls.calculate_kd(player),
                            "avg_ping": player.ping,
                            "minutes_on_server": player.minutes_on_server,
                        }
                    )

        new_players = cls._update_tf2_hours(new_players)
        new_players = cls._update_vac_hours(new_players, steam_bans_data)

        return {"map": cls.map_name, "server_address": cls.server_ip, "players": new_players}

    @staticmethod
    def _get_melee_kill_percentage(player: Player) -> str:
        if player.melee_kills == 0:
            return "no data"

        percentage = round(player.crit_melee_kills / player.melee_kills * 100, 2)

        return f"Melee crit kill {player.crit_melee_kills}/{player.melee_kills} ({percentage}%)"

    @classmethod
    def _update_tf2_hours(cls, to_update_players_list):
        hours_url: List[SteamHoursApiUrlID64] = []
        for player in cls.players:
            hours_url.append(
                SteamHoursApiUrlID64(
                    f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?key={config.STEAM_WEBAPI_KEY}"
                    f"&steamid={player.steamid64}&include_appinfo=false&include_played_free_games=true"
                    f"&appids_filter[0]=440",
                    player.steamid64,
                )
            )

        results_total_game_hours = BulkSteamGameDetailsUrlDownloader(hours_url).download_all()

        for response, steamid64 in results_total_game_hours:
            for player in to_update_players_list:
                if player["steam"]["steamid64"] == steamid64:
                    try:
                        player["steam"]["hours_in_team_fortress_2"] = (
                            str(round(response["response"]["games"][0]["playtime_forever"] / 60))
                            + " hours"
                        )
                    except KeyError:
                        pass

        return to_update_players_list

    @classmethod
    def _update_vac_hours(cls, to_update_players_list, steam_bans_data):
        for player_ban_data in steam_bans_data:
            for player in to_update_players_list:
                if player["steam"]["steamid64"] == player_ban_data.get("SteamId"):
                    try:
                        vac_status = player_ban_data.get("VACBanned", "unknown")
                        number_of_bans = player_ban_data.get("NumberOfVACBans", "unknown")
                        days_since_last_ban = player_ban_data.get("DaysSinceLastBan", "unknown")

                        vac = {
                            "is_VAC_banned": vac_status,
                            "number_of_bans": number_of_bans,
                            "days_since_last_ban": days_since_last_ban,
                        }

                        player["steam"]["VAC"] = vac
                    except KeyError as e:
                        main_logger.warning(f"Failed to fetch vac hours [{e}]")

        return to_update_players_list

    @staticmethod
    def calculate_kd(player: Player) -> float:
        if player.deaths == 0:
            kd = player.kills
        else:
            kd = round(player.kills / player.deaths, 2)
        return kd
