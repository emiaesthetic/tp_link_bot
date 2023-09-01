from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

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
