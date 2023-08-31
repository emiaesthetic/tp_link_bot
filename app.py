import asyncio

from aiogram import Bot, Dispatcher

from src.configreader import config


async def main():
    bot: Bot = Bot(token=config.bot_token)
    dp: Dispatcher = Dispatcher()

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())