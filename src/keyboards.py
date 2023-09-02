from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.lexicon import LEXICON_EN
from src.services.sessions import Device


def create_keyboard(
    devices: list[Device], prefix="add"
) -> InlineKeyboardMarkup:
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    for index, device in enumerate(devices, 1):
        builder.row(
            InlineKeyboardButton(
                text=(f"{index}. MAC-address: {device.mac_address}"),
                callback_data=f"{prefix} {device.mac_address}",
            )
        )
    builder.row(
        InlineKeyboardButton(text=LEXICON_EN["cancel"], callback_data="cancel")
    )
    return builder.as_markup()
