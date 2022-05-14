import os
from dotenv import load_dotenv
import logging
from aiogram.types import BotCommand
from aiogram import Bot, Dispatcher, executor, types, asyncio
# from aiogram.utils.exceptions import BotCommand
# from rooms import room_start
from app.handlers.common import register_handlers_common
from app.handlers.rooms import register_handlers_room
from aiogram.contrib.fsm_storage.memory import MemoryStorage


logger = logging.getLogger(__name__)


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description='Start'),
        BotCommand(command="/rooms", description='Rooms'),
        BotCommand(command="/cancel", description='Cancel the current action')
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
    register_handlers_room(dp)

    await set_commands(bot)

    await dp.start_polling()

if __name__ == "__main__":
    asyncio.run(main())
