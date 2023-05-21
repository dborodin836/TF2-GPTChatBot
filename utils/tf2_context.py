import datetime
import time
from typing import List
from statistics import mean
import requests

from config import config
from utils.types import Player, SteamHoursApiUrlID64
from utils.bulk_url_downloader import BulkSteamGameDetailsUrlDownloader


def steamid3_to_steamid64(steamid3: str) -> int:
    for ch in ['[', ']']:
        if ch in steamid3:
            steamid3 = steamid3.replace(ch, '')

    steamid3_split = steamid3.split(':')
    steamid64 = int(steamid3_split[2]) + 76561197960265728

    return steamid64


def get_date(epoch: int) -> str:
    birthdate = datetime.date.fromtimestamp(epoch)
    current_date = datetime.date.today()

    age_years = current_date.year - birthdate.year - (
            (current_date.month, current_date.day) < (birthdate.month, birthdate.day))
    age_months = current_date.month - birthdate.month - (current_date.day < birthdate.day)
    if age_months < 0:
        age_years -= 1
        age_months += 12
    age_days = (current_date - birthdate.replace(year=current_date.year)).days
    # Get the age tuple in years, months, and days
    age = datetime.timedelta(days=age_days)
    age_years, remainder_days = divmod(age.days, 365)
    age_months, remainder_days = divmod(remainder_days, 30)
    age_days = remainder_days
    age_years = current_date.year - birthdate.year - (
            (current_date.month, current_date.day) < (birthdate.month, birthdate.day))
    return f"{age_years} years {age_months} months {age_days} days"


class StatsData:
    players: List[Player] = []
    map_name: str | None = None
    server_ip: str | None = None

    @classmethod
    def set_map_name(cls, map_name: str) -> None:
        cls.map_name = map_name
        print(f"MAP CHANGED {map_name}")
        cls._reset_players()

    @classmethod
    def set_server_ip(cls, ip: str) -> None:
        cls.server_ip = ip

    @classmethod
    def _reset_players(cls) -> None:
        cls.players = []
        print("RESET PLAYERS")

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

                # print(f"Updated players time on server {player['name']}")
                return

        new_player.steamid64 = steamid3_to_steamid64(new_player.steamid3)
        cls.players.append(new_player)
        # print(f"Added new player {new_player.name} with {new_player.minutes_on_server} minutes on server")

    @classmethod
    def process_kill(cls, killer_username: str, victim_username: str) -> None:
        print(f"'{killer_username}' killed '{victim_username}'")
        for player in cls.players:
            if player.name == killer_username:
                player.kills += 1
                print(f"Incremented kills for a player {player.name}, current value {player.kills}")
            elif player.name == victim_username:
                player.deaths += 1
                print(f"Incremented deaths for a player {player.name}, current value {player.deaths}")

    @classmethod
    def process_kill_bind(cls, username: str) -> None:
        print(f"{username} suicided")
        for player in cls.players:
            if player.name == username:
                player.deaths += 1
                print(f"Incremented deaths for a player {player.name}, current value {player.deaths}")

    @classmethod
    def _get_steam_prfiles_data(cls) -> List[dict]:
        steamids64: List[str] = [str(player.steamid64) for player in cls.players if player.steamid64 is not None]

        try:
            response = requests.get(
                f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={config.STEAM_WEBAPI_KEY}&steamids={','.join(steamids64)}").json()
            return response["response"]["players"]
        except Exception as e:
            print(e, "123131")
            return []

    @classmethod
    def get_data(cls) -> dict:
        new_players: List = []

        # Filter players, exclude those who disconnected
        cls.players = [player for player in cls.players if time.time() - int(player.last_updated) < 120]
        steam_profiles_data_list = cls._get_steam_prfiles_data()

        for player in cls.players:
            account_age, country, real_name = 'unknown', 'unknown', ""

            for player_steam_data in steam_profiles_data_list:
                if str(player.steamid64) == player_steam_data.get("steamid"):
                    try:
                        account_age = get_date(int(player_steam_data["timecreated"]))
                    except KeyError:
                        account_age = 'unknown'

                    country = player_steam_data.get("loccountrycode", "unknown")
                    real_name = player_steam_data.get("realname", "")

            new_players.append({
                "name": player.name,
                "steam": {
                    "steamid64": player.steamid64,
                    "steam_account_age": account_age,
                    "hours_in_team_fortress_2": "unknown",
                    "country": country,
                    "real_name": real_name
                },
                "deaths": player.deaths,
                "kills": player.kills,
                "k/d": cls.calculate_kd(player),
                "avg_ping": player.ping,
                "minutes_on_server": player.minutes_on_server
            })

        new_players = cls._update_tf2_hours(new_players)

        return {
            'map': cls.map_name,
            "server_address": cls.server_ip,
            "players": new_players
        }

    @classmethod
    def _update_tf2_hours(cls, to_update_players_list):
        hours_url: List[SteamHoursApiUrlID64] = []
        for player in cls.players:
            hours_url.append(
                SteamHoursApiUrlID64(
                    f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?key={config.STEAM_WEBAPI_KEY}\
                    &steamid={player.steamid64}&include_appinfo=false&include_played_free_games=true\
                    &appids_filter[0]=440",
                    player.steamid64)
            )

        results_total_game_hours = BulkSteamGameDetailsUrlDownloader(hours_url).download_all()

        for response, steamid64 in results_total_game_hours:
            for player in to_update_players_list:
                if player["steam"]["steamid64"] == str(steamid64):
                    try:
                        player["steam"]["hours_in_team_fortress_2"] = str(
                            round(response["response"]["games"][0]["playtime_forever"] / 60)) + ' hours'
                    except KeyError:
                        pass

        return to_update_players_list

    @staticmethod
    def calculate_kd(player: Player) -> float:
        if player.deaths == 0:
            kd = player.kills
        else:
            kd = round(player.kills / player.deaths, 2)
        return kd
