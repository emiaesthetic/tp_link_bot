from aiogram import Bot
from aiogram.types import BotCommand


async def set_commands(bot: Bot):
    data = [
        BotCommand(command="/start", description="Start new dialog"),
        BotCommand(command="/help", description="Show help"),
        BotCommand(command="/devices", description="Show all devices"),
        BotCommand(command="/reboot", description="Reboot router"),
    ]

    await bot.set_my_commands(data)
