import os
from dotenv import load_dotenv
import logging
from aiogram.types import BotCommand
from aiogram import Bot, Dispatcher, asyncio

from app.handlers.common import register_handlers_common
from aiogram.contrib.fsm_storage.memory import MemoryStorage


logger = logging.getLogger(__name__)


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description='Start'),
        BotCommand(command="/rooms", description='Rooms'),
    ]
    await bot.set_my_commands(commands)


async def main():
    load_dotenv()

    secret_token = os.getenv('TOKEN')

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)
    logger.error("Starting bot")

    bot = Bot(secret_token)
    dp = Dispatcher(bot, storage=MemoryStorage())

    register_handlers_common(dp)

    await set_commands(bot)

    await dp.start_polling()

if __name__ == "__main__":
    asyncio.run(main())
