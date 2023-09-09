import asyncio

from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message

from src.configreader import config
from src.filters import IsAdmin, IsEditCallbackData, IsMacAddressCallbackData
from src.keyboards import create_keyboard
from src.lexicon import LEXICON_EN
from src.services.sessions import session

router: Router = Router()


@router.message(~IsAdmin())
async def process_outside_user_command(message: Message):
    await message.answer(LEXICON_EN["outside_user"])


@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(LEXICON_EN[message.text])


@router.message(Command(commands=["help"]))
async def process_help_command(message: Message):
    await message.answer(LEXICON_EN[message.text])


@router.message(Command(commands=["devices"]))
async def process_devices_command(message: Message):
    white_list = session.get_wireless_connected_devices()
    black_list = session.get_blacklisted_devices()
    await message.answer(
        text=LEXICON_EN[message.text],
        reply_markup=create_keyboard(white_list, black_list),
    )


@router.message(Command(commands=["reboot"]))
async def process_reboot_command(message: Message):
    await message.answer(text=LEXICON_EN["wait"])
    session.reboot()
    await asyncio.sleep(55)
    await message.answer(text=LEXICON_EN["after_waiting"])


@router.callback_query(IsEditCallbackData("add"), IsMacAddressCallbackData())
async def process_add_press(callback: CallbackQuery):
    mac_address = callback.data.split()[-1]
    session.add_device_to_blacklist(mac_address)
    await callback.answer()


@router.callback_query(IsEditCallbackData("remove"), IsMacAddressCallbackData())
async def process_remove_press(callback: CallbackQuery):
    mac_address = callback.data.split()[-1]
    session.removed_device_from_blacklist(mac_address)
    await callback.answer()


@router.callback_query(F.data == "update")
async def process_update_press(callback: CallbackQuery):
    white_list = session.get_wireless_connected_devices()
    black_list = session.get_blacklisted_devices()
    try:
        await callback.message.edit_text(
            text=LEXICON_EN["/devices"],
            reply_markup=create_keyboard(white_list, black_list),
        )
    except TelegramBadRequest:
        await callback.answer()


@router.message()
async def process_other_message(message: Message):
    await message.answer(text=LEXICON_EN["other"])
