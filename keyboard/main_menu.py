from aiogram import Bot
from aiogram.types import BotCommand

from lexicon.lexicon import LEXICON_COMMANDS


async def setup_bot_commands(bot: Bot):
    main_menu_commands = [BotCommand(command=command, description=description)
                          for command, description in LEXICON_COMMANDS.items()]
    await bot.set_my_commands(commands=main_menu_commands, language_code='ru')
