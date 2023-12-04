import asyncio
import os
from aiogram import Bot, Dispatcher
from keyboard.main_menu import setup_bot_commands
from handlers import user_handlers, other_handlers
from dotenv import load_dotenv

load_dotenv()

bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher()

dp.include_router(user_handlers.router)
dp.include_router(other_handlers.router)


async def start():
    try:
        await setup_bot_commands(bot)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(start())
