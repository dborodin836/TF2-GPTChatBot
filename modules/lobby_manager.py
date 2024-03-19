import difflib
import re
import time
from statistics import mean
from typing import Any, List, Optional

import requests

from config import config
from modules.bulk_url_downloader import BulkSteamGameDetailsUrlDownloader
from modules.typing import Player, SteamHoursApiUrlID64
from modules.logs import get_logger
from modules.utils.steam import steamid3_to_steamid64
from modules.utils.time import get_date, get_minutes_from_str

main_logger = get_logger("main")
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


def find_username(username: str, data: List) -> Optional[str] | Any:
    if len(data) == 0:
        return None
    matches = []

    for candidate in data:
        if candidate in username:
            matches.append(candidate)

    if len(matches) == 1:
        return matches[0]

    diff = difflib.get_close_matches(username, matches, n=1, cutoff=0.8)
    if len(diff) == 0:
        return None
    if type(diff) is str:
        return diff
    elif type(diff) is list:
        return diff[0]


class LobbyManager:
    def __init__(self):
        self.players: List[Player] = list()
        self.server_ip: Optional[str] = None

    def get_player_by_name(self, username: str) -> Optional[Player]:
        for plr in self.players:
            if plr.name == username:
                return plr
        return None

    def search_username(self, username: str) -> str:
        data = [plr.name for plr in self.players]
        usr = find_username(username, data)
        if usr is not None:
            return usr
        return username

    def is_username_exist(self, username: str) -> bool:
        for player in self.players:
            if username == player.name:
                return True

        return False

    def add_player(self, new_player: Player) -> None:
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

        # New player
        new_player.steamid64 = steamid3_to_steamid64(new_player.steamid3)
        self.players.append(new_player)
        main_logger.debug(
            f"Added new player {new_player.name} with {new_player.minutes_on_server} minutes on server"
        )

    @property
    def map(self):
        return self.map

    @map.setter
    def map(self, value: str) -> None:
        self.map = value
        combo_logger.info(f"MAP CHANGE DETECTED {value}")
        self.reset()

    def reset(self) -> None:
        self.players.clear()
        combo_logger.info("RESET PLAYERS")

    def handle_kill_bind(self, player: Player) -> None:
        main_logger.debug(f"{player.name} suicided")
        player.deaths += 1
        main_logger.trace(
            f"Incremented deaths for a player {player.name}, current value {player.deaths}"
        )

    def handle_kill(
            self, killer: Player, victim: Player, weapon: str, is_crit: bool
    ) -> None:
        main_logger.debug(
            f"'{killer.name}' killed '{victim.name} with {weapon} {'crit' if is_crit else ''}'"
        )

        # Update killer stats
        if weapon in MELEE_WEAPONS_KILL_IDS:
            killer.melee_kills += 1
            if is_crit:
                killer.crit_melee_kills += 1
        killer.kills += 1
        main_logger.trace(
            f"Incremented kills for a player {killer.name}, current value {killer.kills}"
        )

        # Update victim stats
        victim.deaths += 1
        main_logger.trace(
            f"Incremented deaths for a player {victim.name}, current value {victim.deaths}"
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
                            "melee_crit_percentage": player.melee_crit_kills_percentage,
                            "k/d": player.kd,
                            "avg_ping": player.ping,
                            "minutes_on_server": player.minutes_on_server,
                        }
                    )

        new_players = self._update_tf2_hours(new_players)
        new_players = self._update_vac_hours(new_players, steam_bans_data)

        return {
            "map": self.map,
            "server_address": self.server_ip,
            "players": new_players,
        }

    def stats_regexes(self, line: str):
        # Parsing user line from status command
        if matches := re.search(
                r"^#\s*\d*\s*\"(.*)\"\s*(\[.*])\s*(\d*:?\d*:\d*)\s*(\d*)\s*\d*\s*\w*\s*\w*",
                line,
        ):
            time_on_server = matches.groups()[2]

            time_ = get_minutes_from_str(time_on_server)

            player = Player(
                name=matches.groups()[0],
                minutes_on_server=time_,
                last_updated=time_,
                steamid3=matches.groups()[1],
                ping=matches.groups()[3],
            )

            self.add_player(player)

        # Parsing map name on connection
        elif matches := re.search(r"^Map:\s(\w*)", line):
            map_ = matches.groups()[0]
            self.map = map_

        # Parsing server ip
        elif matches := re.search(r"^udp/ip\s*:\s*((\d*.){4}:\d*)", line):
            ip = matches.groups()[0]
            main_logger.info(f"Server ip is [{ip}]")
            self.server_ip = ip

        # Parsing kill
        elif matches := re.search(r"^(.*)\skilled\s(.*)\swith\s(\w*).", line):
            killer = matches.groups()[0]
            victim = matches.groups()[1]
            weapon = matches.groups()[2]
            is_crit = line.strip().endswith("(crit)")

            plr_killer = self.get_player_by_name(killer)
            plr_victim = self.get_player_by_name(victim)

            if plr_victim is not None and plr_killer is not None:
                self.handle_kill(plr_killer, plr_victim, weapon, is_crit)

        # Parsing suicide
        elif matches := re.search(r"^(.*)\ssuicided", line):
            username = matches.groups()[0]
            player = self.get_player_by_name(username)
            if player is not None:
                self.handle_kill_bind(player)


lobby_manager = LobbyManager()
