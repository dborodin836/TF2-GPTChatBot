from modules.bans import BansManager
from modules.command_controllers import InitializerConfig
from modules.lobby_manager import LobbyManager
import modules.lobby_manager
from tests.common import MockConfig, get_player, temp_file
from modules.commands.gui.bans import handle_ban, handle_unban, handle_list_bans


def test_handle_ban(temp_file, mocker):
    conf = MockConfig()
    lobby_manager = LobbyManager()
    bans_manager = BansManager(temp_file)
    mocker.patch.object(modules.lobby_manager, "config", conf)
    mocker.patch.object(modules.commands.gui.bans, "lobby_manager", lobby_manager)
    mocker.patch.object(modules.commands.gui.bans, "bans_manager", bans_manager)

    plr1 = get_player("player1", 1)
    plr2 = get_player("player2", 2)
    lobby_manager.add_player(plr1)
    lobby_manager.add_player(plr2)

    handle_ban("ban player1", InitializerConfig())

    assert bans_manager.is_banned_player(plr1) is True
    assert bans_manager.is_banned_player(plr2) is False


def test_handle_unban(temp_file, mocker):
    conf = MockConfig()
    lobby_manager = LobbyManager()
    bans_manager = BansManager(temp_file)
    mocker.patch.object(modules.lobby_manager, "config", conf)
    mocker.patch.object(modules.commands.gui.bans, "lobby_manager", lobby_manager)
    mocker.patch.object(modules.commands.gui.bans, "bans_manager", bans_manager)

    plr1 = get_player("player1", 1)
    plr2 = get_player("player2", 2)
    lobby_manager.add_player(plr1)
    lobby_manager.add_player(plr2)

    handle_ban("ban player1", InitializerConfig())

    assert bans_manager.is_banned_player(plr1) is True
    assert bans_manager.is_banned_player(plr2) is False

    handle_unban("unban player1", InitializerConfig())
    assert bans_manager.is_banned_player(plr1) is False
    assert bans_manager.is_banned_player(plr2) is False
