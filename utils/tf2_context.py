from typing import List
from statistics import mean

from utils.types import Player


def steamid3_to_steamid64(steamid3: str) -> int:
    for ch in ['[', ']']:
        if ch in steamid3:
            steamid3 = steamid3.replace(ch, '')

    steamid3_split = steamid3.split(':')
    steamid64 = int(steamid3_split[2]) + 76561197960265728

    return steamid64


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
                player.last_updated = new_player.last_updated

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
        for player in cls.players:

            # Remove players that left the game
            if player.minutes_on_server > player.last_updated:
                continue

            # Calculate K/D
            if player.deaths == 0:
                kd = player.kills
            else:
                kd = round(player.kills / player.deaths, 2)

            new_players.append({
                "name": player.name,
                "deaths": player.deaths,
                "kills": player.kills,
                "k/d": kd,
                "avg_ping": player.ping,
                "minutes_on_server": player.minutes_on_server
            })

        data = {
            'map': cls.map_name,
            "server_address": cls.server_ip,
            "players": new_players
        }
        return data
