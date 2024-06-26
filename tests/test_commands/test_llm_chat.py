import modules.servers.tf2
import modules.utils.text
from modules.builder.utils import create_command_from_dict
from modules.command_controllers import InitializerConfig
from modules.commands.llm import LLMChatCommand
from modules.conversation_history import ConversationHistory
from modules.typing import LogLine
from tests.common import DummyProvider, MockConfig, get_player


def dummy_func(*args):
    return args


def test_command_hard_limit(mocker):
    config = MockConfig()
    mocker.patch.object(modules.commands.base, "send_say_command_to_tf2", dummy_func)
    mocker.patch.object(modules.servers.tf2, "config", config)
    mocker.patch.object(modules.utils.text, "config", config)
    spy = mocker.spy(modules.commands.base, "send_say_command_to_tf2")
    chat_settings_shared = {
        "enable-hard-limit": True,
        "hard-limit-length": 4,
    }
    chat = ConversationHistory(chat_settings_shared)

    class TestCmd(LLMChatCommand):
        provider = DummyProvider
        settings = chat_settings_shared

        @classmethod
        def get_chat(cls, logline: LogLine, shared_dict: InitializerConfig) -> ConversationHistory:
            return chat

    player_1 = get_player("test", 1)
    logline = LogLine(username="test", prompt="2+2", player=player_1, is_team_message=False)

    func = TestCmd.as_command()
    func(logline, InitializerConfig())

    assert spy.call_count == 1
    assert spy.spy_return == ("comp...", "test", False)

    chat_settings_new = {"enable-hard-limit": False, "hard-limit-length": 4}
    TestCmd.chat_settings = chat_settings_new
    func(logline, InitializerConfig())
    assert spy.call_count == 2
    assert spy.spy_return == ("completion text", "test", False)


def test_multiple_commands_global():
    cmd_dict_1 = {
        "name": "test_1",
        "prefix": "!",
        "provider": "text-generation-webui",
        "type": "command-global",
        "traits": [{"empty-prompt-message-response": {"msg": "EMPTY TEST_1 RESPONSE"}}],
    }
    cmd_dict_2 = {
        "name": "test_2",
        "prefix": "!",
        "provider": "text-generation-webui",
        "type": "command-global",
        "traits": [{"empty-prompt-message-response": {"msg": "EMPTY TEST_2 RESPONSE"}}],
    }
    command_1 = create_command_from_dict(cmd_dict_1)
    command_2 = create_command_from_dict(cmd_dict_2)

    assert command_1.name != command_2.name
    assert command_1.wrappers != command_2.wrappers


def test_multiple_commands_private():
    cmd_dict_1 = {
        "name": "test_1",
        "prefix": "!",
        "provider": "text-generation-webui",
        "type": "command-private",
        "traits": [{"empty-prompt-message-response": {"msg": "EMPTY TEST_1 RESPONSE"}}],
    }
    cmd_dict_2 = {
        "name": "test_2",
        "prefix": "!",
        "provider": "text-generation-webui",
        "type": "command-private",
        "traits": [{"empty-prompt-message-response": {"msg": "EMPTY TEST_2 RESPONSE"}}],
    }
    command_1 = create_command_from_dict(cmd_dict_1)
    command_2 = create_command_from_dict(cmd_dict_2)

    assert command_1.name != command_2.name
    assert command_1.wrappers != command_2.wrappers


def test_multiple_commands_quick():
    cmd_dict_1 = {
        "name": "test_1",
        "prefix": "!",
        "provider": "text-generation-webui",
        "type": "quick-query",
        "traits": [{"empty-prompt-message-response": {"msg": "EMPTY TEST_1 RESPONSE"}}],
    }
    cmd_dict_2 = {
        "name": "test_2",
        "prefix": "!",
        "provider": "text-generation-webui",
        "type": "quick-query",
        "traits": [{"empty-prompt-message-response": {"msg": "EMPTY TEST_2 RESPONSE"}}],
    }
    command_1 = create_command_from_dict(cmd_dict_1)
    command_2 = create_command_from_dict(cmd_dict_2)

    assert command_1.name != command_2.name
    assert command_1.wrappers != command_2.wrappers
