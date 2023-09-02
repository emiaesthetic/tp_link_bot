from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message

from src.filters import IsMacAddress
from src.keyboards import create_keyboard
from src.lexicon import LEXICON_EN
from src.services.sessions import session

router: Router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(LEXICON_EN[message.text])


@router.message(Command(commands=["help"]))
async def process_help_command(message: Message):
    await message.answer(LEXICON_EN[message.text])


@router.message(Command(commands=["devices"]))
async def process_devices_command(message: Message):
    text = session.show_wireless_connected_devices()
    await message.answer(text=text)


@router.message(Command(commands=["blacklist"]))
async def process_blacklist_command(message: Message):
    text = session.show_blacklisted_devices()
    await message.answer(text=text)


@router.message(Command(commands=["add"]))
async def process_add_command(message: Message):
    await message.answer(
        text=LEXICON_EN[message.text],
        reply_markup=create_keyboard(session.get_wireless_connected_devices()),
    )


@router.message(Command(commands=["remove"]))
async def process_remove_command(message: Message):
    await message.answer(
        text=LEXICON_EN[message.text],
        reply_markup=create_keyboard(
            session.get_blacklisted_devices(), "remove"
        ),
    )


@router.callback_query(IsMacAddress())
async def process_mac_address_press(callback: CallbackQuery):
    prefix, mac_address = callback.data.split()
    if prefix == "add":
        session.add_device_to_blacklist(mac_address)
    else:
        session.removed_device_from_blacklist(mac_address)
    await callback.message.edit_text(text=LEXICON_EN["/help"])
    await callback.answer()


@router.callback_query(F.data == "cancel")
async def process_cancel_press(callback: CallbackQuery):
    await callback.message.edit_text(text=LEXICON_EN["/help"])
    await callback.answer()
