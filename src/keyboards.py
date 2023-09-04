from typing import Optional

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.lexicon import DEVICE_STATUS, LEXICON_EN
from src.services.sessions import Device


def create_keyboard(
    white_list: list[Optional[Device]], black_list: list[Optional[Device]]
) -> InlineKeyboardMarkup:
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    for device in white_list:
        builder.row(
            InlineKeyboardButton(
                text=f"{DEVICE_STATUS['ON']} MAC-address: {device.mac_address}",
                callback_data=f"add {device.mac_address}",
            )
        )
    for device in black_list:
        builder.row(
            InlineKeyboardButton(
                text=f"{DEVICE_STATUS['OFF']} MAC-address: {device.mac_address}",
                callback_data=f"remove {device.mac_address}",
            )
        )
    builder.row(
        InlineKeyboardButton(text=LEXICON_EN["update"], callback_data="update")
    )
    return builder.as_markup()
