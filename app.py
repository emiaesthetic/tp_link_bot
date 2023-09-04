import asyncio
import logging

from aiogram import Bot, Dispatcher

from src import user_handers
from src.commands import set_commands
from src.configreader import config

logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s "
        "[%(asctime)s] - %(name)s - %(message)s",
    )

    logger.info("Starting bot")

    bot: Bot = Bot(token=config.bot_token, parse_mode="HTML")
    dp: Dispatcher = Dispatcher()

    await set_commands(bot)

    dp.include_router(user_handers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
