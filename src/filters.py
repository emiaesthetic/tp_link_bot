import re

from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery, Message

from src.configreader import config


class IsMacAddressCallbackData(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        pattern = r"^([0-9A-F]{2}[:]){5}([0-9A-F]{2})$"
        allowed = re.compile(pattern=pattern, flags=re.IGNORECASE)
        return bool(allowed.fullmatch(callback.data.split()[-1]))


class IsEditCallbackData(BaseFilter):
    def __init__(self, operation: str) -> None:
        self.operation = operation

    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data.startswith(self.operation)


class IsAdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id == int(config.admin_id)
