import datetime
import time
from typing import List
from statistics import mean

from config import config
from utils.types import Player
from requests.sessions import Session
from threading import Thread, local
from queue import Queue
import requests


def steamid3_to_steamid64(steamid3: str) -> int:
    for ch in ['[', ']']:
        if ch in steamid3:
            steamid3 = steamid3.replace(ch, '')

    steamid3_split = steamid3.split(':')
    steamid64 = int(steamid3_split[2]) + 76561197960265728

    return steamid64


q = Queue(maxsize=0)  # Use a queue to store all URLs
results = []
thread_local = local()  # The thread_local will hold a Session object


def get_session() -> Session:
    if not hasattr(thread_local, 'session'):
        thread_local.session = requests.Session()  # Create a new Session if not exists
    return thread_local.session


def download_link() -> None:
    """download link worker, get URL from queue until no url left in the queue"""
    session = get_session()
    while True:
        url = q.get()
        with session.get(url[0]) as response:
            results.append((response.json(), url[1]))
        q.task_done()  # tell the queue, this url downloading work is done


def download_all(urls) -> None:
    """Start 10 threads, each thread as a wrapper of downloader"""
    thread_num = 10
    for i in range(thread_num):
        t_worker = Thread(target=download_link)
        t_worker.start()
    q.join()  # main thread wait until all url finished downloading


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
        cls.reset_players()

    @classmethod
    def set_server_ip(cls, ip: str) -> None:
        cls.server_ip = ip

    @classmethod
    def reset_players(cls) -> None:
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
        print(f"Added new player {new_player.name} with {new_player.minutes_on_server} minutes on server")

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
    def process_killbind(cls, username: str) -> None:
        print(f"{username} suicided")
        for player in cls.players:
            if player.name == username:
                player.deaths += 1
                print(f"Incremented deaths for a player {player.name}, current value {player.deaths}")

    @classmethod
    def get_data(cls) -> dict:
        new_players: list = []
        hours_url = []

        steamids64: List[str] = [str(player.steamid64) for player in cls.players if player.steamid64 is not None]

        try:
            response = requests.get(
                f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={config.STEAM_WEBAPI_KEY}&steamids={','.join(steamids64)}").json()
            steam_players = response["response"]["players"]

        except Exception as e:
            steam_players = []
            print(e)

        for player in cls.players:
            # Ignore players that left the game
            print(f"player {player.name} {player.minutes_on_server=} {player.last_updated}")
            if time.time() - int(player.last_updated) > 120:
                print("print skipped a player")
                continue

            hours_url.append(
                (f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?key={config.STEAM_WEBAPI_KEY}&steamid={player.steamid64}&include_appinfo=false&include_played_free_games=true&appids_filter[0]=440",
                 player.steamid64))

            country, real_name, account_age = "unknown", "unknown", "unknown"
            id64 = 0

            for pl in steam_players:
                if str(player.steamid64) == pl["steamid"]:
                    try:
                        account_age = get_date(int(pl["timecreated"]))
                    except KeyError:
                        account_age = 'unknown'
                    try:
                        country = pl["loccountrycode"]
                    except KeyError:
                        country = 'unknown'
                    try:
                        real_name = pl["realname"]
                    except KeyError:
                        real_name = ''
                    id64 = pl["steamid"]

            # Calculate K/D
            if player.deaths == 0:
                kd = player.kills
            else:
                kd = round(player.kills / player.deaths, 2)

            new_players.append({
                "name": player.name,
                "steam": {
                    "steamid64": id64,
                    "steam_account_age": account_age,
                    "hours_in_team_fortress_2": "unknown",
                    "country": country,
                    "real_name": real_name
                },
                "deaths": player.deaths,
                "kills": player.kills,
                "k/d": kd,
                "avg_ping": player.ping,
                "minutes_on_server": player.minutes_on_server
            })

        for url in hours_url:
            q.put(url)

        print("starting downloading urls")

        download_all(hours_url)

        print("updating urls")

        for res, id64 in results:
            for player in new_players:
                if player["steam"]["steamid64"] == str(id64):
                    try:
                        player["steam"]["hours_in_team_fortress_2"] = str(round(res["response"]["games"][0]["playtime_forever"] / 60)) + ' hours'
                    except KeyError:
                        pass

        data = {
            'map': cls.map_name,
            "server_address": cls.server_ip,
            "players": new_players
        }
        return data
