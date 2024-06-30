import time
from collections import deque
from dataclasses import dataclass


@dataclass
class UserState:
    username: str
    calls: int = 0


@dataclass
class CommandState:
    name: str
    calls: int = 0


class CommandMonitor:
    def __init__(self, window_size=60):
        self.window_size = window_size
        self.command_times = deque()
        self.users = []
        self.commands = []

    def record_call(self, username: str, command: str):
        current_time = time.time()
        self.command_times.append(current_time)
        self._remove_old_commands(current_time)

        for user_state in self.users:
            if user_state.username == username:
                user_state.calls += 1
                break
        else:
            self.users.append(UserState(username, 1))

        for command_state in self.commands:
            if command_state.name == command:
                command_state.calls += 1
                break
        else:
            self.commands.append(CommandState(command, 1))

    def _remove_old_commands(self, current_time):
        # Remove commands outside the time window
        while self.command_times and (current_time - self.command_times[0] > self.window_size):
            self.command_times.popleft()

    def get_commands_per_minute(self):
        self._remove_old_commands(time.time())
        return len(self.command_times)

    def get_users(self, n: int = 5):
        return sorted(self.users, key=lambda x: x.calls, reverse=True)[:n]

    def get_commands(self, n: int = 5):
        return sorted(self.commands, key=lambda x: x.calls, reverse=True)[:n]


monitor = CommandMonitor()
