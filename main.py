import asyncio
import os
from aiogram import Bot, types, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.filters.command import Command
from aiogram.utils.markdown import text, bold, italic
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from dotenv import load_dotenv

load_dotenv()

bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher()


async def start():
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


@dp.message(Command("start"))
async def process_start_command(message: types.Message):
    msg = text(bold('      ГЛАВНОЕ МЕНЮ'),
               italic('Что вы хотите изучать?:'), sep='\n')
    button_hi = InlineKeyboardButton(text='Упражнение с 1 до 100',
                                     callback_data='multi')

    keyboard = [[button_hi]]

    greet_kb1 = InlineKeyboardMarkup(inline_keyboard=keyboard)
    await bot.send_message(message.from_user.id, msg, parse_mode=ParseMode.MARKDOWN, reply_markup=greet_kb1)


@dp.message(Command("help"))
async def process_help_command(message: types.Message):
    msg = text(bold("Упражнение с 1 до 100"), italic("ОПИСАНИЕ:"),
               bold("Умножение") + " с 1 до 10",
               bold("Деление") + " с 1 до 10",
               bold("Вычитание") + " с 1 до 100",
               bold("Сложение") + " с 1 до 100",
               "в разброс. Вопросы не повторяются.",
               "Завершить тестирование можно в любой момент",
               "нажав кнопку Завершить",
               "Предлагается 5 вариантов ответа.",
               italic("Вы готовы начать упражнения?:"), sep='\n')
    button_hi = InlineKeyboardButton(text='Приступить',
                                     callback_data='start_multi')
    button_end = InlineKeyboardButton(text='Завершить',
                                      callback_data='results')

    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(button_hi, width=1)
    kb_builder.row(button_end)
    greet_kb1 = kb_builder.as_markup()
    await bot.send_message(message.from_user.id, msg, parse_mode=ParseMode.MARKDOWN, reply_markup=greet_kb1)


@dp.callback_query(F.data == 'start')
async def callback_query_handler(callback_query: types.CallbackQuery):
    msg = text(bold('      ГЛАВНОЕ МЕНЮ'),
               italic('Что вы хотите изучать?:'), sep='\n')
    button_hi = InlineKeyboardButton(text='Упражнение с 1 до 100',
                                     callback_data='multi')

    keyboard = [[button_hi]]

    greet_kb1 = InlineKeyboardMarkup(inline_keyboard=keyboard)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, msg, parse_mode=ParseMode.MARKDOWN, reply_markup=greet_kb1)


@dp.callback_query(F.data == 'multi')
async def callback_query_handler(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Нажата первая кнопка!')


@dp.callback_query(F.data == "start_multi")
async def callback_query_handler(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Напиши мне что-нибудь, и я отправлю этот текст тебе в ответ!")


@dp.callback_query(F.data == "results")
async def callback_query_handler(callback_query: types.CallbackQuery):
    quanty = "10"
    correct = "10"
    uncorrect = "10"
    msg = text(bold("РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ:"),
               bold("Всего решено: ") + quanty,
               bold("Правильных: ") + correct,
               bold("Неправильных: ") + uncorrect, sep='\n')
    button_hi = InlineKeyboardButton(text='Начать снова',
                                     callback_data='multi')
    button_end = InlineKeyboardButton(text='Меню',
                                      callback_data='start')

    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(button_hi, width=1)
    kb_builder.row(button_end)
    greet_kb1 = kb_builder.as_markup()
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, msg, parse_mode=ParseMode.MARKDOWN)
    if uncorrect == "10":
        await bot.send_photo(callback_query.message.chat.id, types.input_file.FSInputFile("./img/five.jpg"))
        await bot.send_message(callback_query.from_user.id, "Что делать дальше?", parse_mode=ParseMode.MARKDOWN, reply_markup=greet_kb1)


@dp.message()
async def echo_message(msg: types.Message):
    await bot.send_message(msg.from_user.id, msg.text)


if __name__ == '__main__':
    asyncio.run(start())
