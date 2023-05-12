class Data:
    players = []
    map_name = None
    server_ip = None

    @classmethod
    def set_map_name(cls, map_name):
        cls.map_name = map_name
        print(f"MAP CHANGED {map_name}")
        cls.reset_players()

    @classmethod
    def set_server_ip(cls, ip: str):
        cls.server_ip = ip
        print(f"CHANGED SERVER {ip}")

    @classmethod
    def reset_players(cls):
        cls.players = []
        print("RESET PLAYERS")

    @classmethod
    def add_player(cls, new_player: dict):
        for player in cls.players:
            if player['name'] == new_player['name']:
                player['minutes_on_server'] = new_player['minutes_on_server']
                # print(f"Updated players time on server {player['name']}")
                return
        cls.players.append(new_player)
        print(f"Added new player {new_player['name']} with {new_player['minutes_on_server']} minutes on server")

    @classmethod
    def process_kill(cls, killer, victim):
        print(f"'{killer}' killed '{victim}'")
        for player in cls.players:
            if player['name'] == killer:
                try:
                    player['kills'] += 1
                    print(f"Incremented kills for a player {player['name']}, current value {player['kills']}")
                except Exception:
                    player['kills'] = 1
                    print(f"First kill for player {player['name']}")
            if player['name'] == victim:
                try:
                    player['deaths'] += 1
                    print(f"Incremented deaths for a player {player['name']}, current value {player['deaths']}")
                except Exception:
                    player['deaths'] = 1
                    print(f"First death for player {player['name']}")

    @classmethod
    def process_killbind(cls, player_name: str):
        print(f"{player_name} suicided")
        for player in cls.players:
            if player['name'] == player_name:
                try:
                    player['deaths'] += 1
                    print(f"Incremented deaths for a player {player['name']}, current value {player['deaths']}")
                except Exception:
                    player['deaths'] = 1
                    print(f"First death for player {player['name']}")

    @classmethod
    def get_data(cls) -> dict:
        dictionary = {
            'map': cls.map_name,
            "server_address": cls.server_ip,
            "players": cls.players
        }
        return dictionary
