from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from src.lexicon import LEXICON_EN

router: Router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(LEXICON_EN[message.text])


@router.message(Command(commands=["help"]))
async def process_help_command(message: Message):
    await message.answer(LEXICON_EN[message.text])
