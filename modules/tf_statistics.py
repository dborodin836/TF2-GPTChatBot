import time
from statistics import mean
from typing import List

import requests

from config import config
from modules.bulk_url_downloader import BulkSteamGameDetailsUrlDownloader
from modules.logs import get_logger
from modules.typing import Player, SteamHoursApiUrlID64
from modules.utils.steam import steamid3_to_steamid64
from modules.utils.time import get_date

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


class StatsData:
    def __init__(self):
        self.players: List[Player] = []
        self.map_name: str | None = None
        self.server_ip: str | None = None

    def set_map_name(self, map_name: str) -> None:
        self.map_name = map_name
        combo_logger.info(f"MAP CHANGE DETECTED {map_name}")
        self._reset_players()

    def set_server_ip(self, ip: str) -> None:
        self.server_ip = ip

    def _reset_players(self) -> None:
        self.players = []
        combo_logger.info("RESET PLAYERS")

    def add_player(self, new_player: Player):
        for player in self.players:
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
        self.players.append(new_player)
        main_logger.debug(
            f"Added new player {new_player.name} with {new_player.minutes_on_server} minutes on server"
        )

    def handle_kill(
            self, killer_username: str, victim_username: str, weapon: str, is_crit: bool
    ) -> None:
        main_logger.debug(
            f"'{killer_username}' killed '{victim_username} with {weapon} {'crit' if is_crit else ''}'"
        )

        for player in self.players:
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

    def process_kill_bind(self, username: str) -> None:
        main_logger.debug(f"{username} suicided")
        for player in self.players:
            if player.name == username:
                player.deaths += 1
                main_logger.trace(
                    f"Incremented deaths for a player {player.name}, current value {player.deaths}"
                )

    def _get_steam_profiles_data(self, steamids64: List[str]) -> List[dict]:
        try:
            response = requests.get(
                f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={config.STEAM_WEBAPI_KEY}&steamids={','.join(steamids64)}"
            ).json()
            return response["response"]["players"]
        except Exception as e:
            main_logger.warning(f"Failed to fetch steam profiles data [{e}]")
            return []

    def _get_steam_ban_data(self, steamids64: List[str]) -> List[dict]:
        try:
            response = requests.get(
                f" http://api.steampowered.com/ISteamUser/GetPlayerBans/v1/?key={config.STEAM_WEBAPI_KEY}&steamids={','.join(steamids64)}"
            ).json()
            return response["players"]
        except Exception as e:
            main_logger.warning(f"Failed to fetch steam bans data [{e}]")
            return []

    def get_data(self) -> dict:
        new_players: List = []

        # Filter players, exclude those who disconnected
        self.players = [
            player for player in self.players if time.time() - int(player.last_updated) < 120
        ]
        id64 = [str(player.steamid64) for player in self.players if player.steamid64 is not None]
        steam_profiles_data_list = self._get_steam_profiles_data(id64)
        steam_bans_data = self._get_steam_ban_data(id64)

        for player in self.players:
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
                            "melee_crit_percentage": self._get_melee_kill_percentage(player),
                            "k/d": self.calculate_kd(player),
                            "avg_ping": player.ping,
                            "minutes_on_server": player.minutes_on_server,
                        }
                    )

        new_players = self._update_tf2_hours(new_players)
        new_players = self._update_vac_hours(new_players, steam_bans_data)

        return {
            "map": self.map_name,
            "server_address": self.server_ip,
            "players": new_players,
        }

    @staticmethod
    def _get_melee_kill_percentage(player: Player) -> str:
        if player.melee_kills == 0:
            return "no data"

        percentage = round(player.crit_melee_kills / player.melee_kills * 100, 2)

        return f"Melee crit kill {player.crit_melee_kills}/{player.melee_kills} ({percentage}%)"

    def _update_tf2_hours(self, to_update_players_list):
        hours_url: List[SteamHoursApiUrlID64] = []
        for player in self.players:
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

    def _update_vac_hours(self, to_update_players_list, steam_bans_data):
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
