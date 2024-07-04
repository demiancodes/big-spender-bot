import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv

from src.bot.handlers import start
from src.bot.setup import set_bot_description

load_dotenv()  # Parses the .env file and then loads all found variables as environment variables


async def main():
    """
    Starts the bot's operation.

    This function initializes the bot with the provided token.
    It sets up a dispatcher to handle incoming updates and includes routers for processing specific
    commands.
    The bot's description is set, and any existing webhook is deleted to ensure smooth polling
    operation.
    Finally, it starts polling for updates.
    """
    bot = Bot(token=getenv("BOT_TOKEN"), default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    dp = Dispatcher()
    dp.include_routers(start.router)

    await set_bot_description(bot)

    await bot.delete_webhook(drop_pending_updates=True)

    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
