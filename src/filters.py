import re

from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery


class IsMacAddressCallbackData(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        pattern = r"^([0-9A-F]{2}[:]){5}([0-9A-F]{2})$"
        allowed = re.compile(pattern=pattern, flags=re.IGNORECASE)
        return bool(allowed.fullmatch(callback.data.split()[-1]))


class IsAddCallbackData(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data.startswith("add")


class IsRemoveCallbackData(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data.startswith("remove")
