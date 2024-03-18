from config import config
from modules.typing import Player


# def check_permission(func):
#     def wrapper(*args, **kwargs):
#         if user_has_permission():
#             return func(*args, **kwargs)
#         else:
#             return "Permission denied"
#
#     return wrapper


def is_admin(user: Player) -> bool:
    if config.HOST_STEAMID3 == user.steamid3:
        return True

    if not config.FALLBACK_TO_USERNAME:
        return False

    if config.HOST_USERNAME == user.name:
        return True

    return False
