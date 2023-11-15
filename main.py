import asyncio
import os
import random
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
    await start_command(message.from_user.id)


@dp.message(Command("help"))
async def process_help_command(message: types.Message):
    await help_command(message.from_user.id)


@dp.callback_query(F.data == 'start')
async def callback_query_handler(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await start_command(callback_query.from_user.id)


@dp.callback_query(F.data == 'help')
async def callback_query_handler(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await help_command(callback_query.from_user.id)


@dp.callback_query(F.data == 'multi')
async def callback_query_handler(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await generate(callback_query.from_user.id)
    # await bot.send_message(callback_query.from_user.id, 'Нажата первая кнопка!')


@dp.callback_query(F.data == 'correct_answer')
async def callback_query_handler(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Вы ответили верно!")
    await generate(callback_query.from_user.id)


@dp.callback_query(F.data == 'answer')
async def callback_query_handler(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Вы ответили неверно!")
    await generate(callback_query.from_user.id)


@dp.callback_query(F.data == "start_multi")
async def callback_query_handler(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Напиши мне что-нибудь, и я отправлю этот текст тебе в ответ!")


@dp.callback_query(F.data == "results")
async def callback_query_handler(callback_query: types.CallbackQuery):
    quanty = "10"
    correct = "10"
    incorrect = "10"
    msg = text(bold("РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ:"),
               bold("Всего решено: ") + quanty,
               bold("Правильных: ") + correct,
               bold("Неправильных: ") + incorrect, sep='\n')
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
    if incorrect == "10":
        await bot.send_photo(callback_query.message.chat.id, types.input_file.FSInputFile("./img/five.jpg"))
        await bot.send_message(callback_query.from_user.id, "Что делать дальше?", parse_mode=ParseMode.MARKDOWN,
                               reply_markup=greet_kb1)


@dp.message()
async def echo_message(msg: types.Message):
    await bot.send_message(msg.from_user.id, msg.text)


async def start_command(user_id: any):
    msg = text(bold('      ГЛАВНОЕ МЕНЮ'),
               italic('Что вы хотите изучать?:'), sep='\n')
    button_hi = InlineKeyboardButton(text='Упражнение с 1 до 100',
                                     callback_data='help')

    keyboard = [[button_hi]]

    greet_kb1 = InlineKeyboardMarkup(inline_keyboard=keyboard)
    await bot.send_message(user_id, msg, parse_mode=ParseMode.MARKDOWN, reply_markup=greet_kb1)


async def help_command(user_id: any):
    msg = text(bold("Упражнение с 1 до 100"), italic("ОПИСАНИЕ:"),
               bold("Умножение") + " с 1 до 10",
               bold("Деление") + " с 1 до 10",
               bold("Вычитание") + " с 1 до 100",
               bold("Сложение") + " с 1 до 100",
               "в разброс. Вопросы не повторяются.",
               "Завершить тестирование можно в любой момент, нажав кнопку Завершить",
               "Предлагается 5 вариантов ответа.",
               italic("Вы готовы начать упражнения?:"), sep='\n')
    button_hi = InlineKeyboardButton(text='Приступить',
                                     callback_data='multi')
    button_end = InlineKeyboardButton(text='Завершить',
                                      callback_data='results')

    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(button_hi, width=1)
    kb_builder.row(button_end)
    greet_kb1 = kb_builder.as_markup()
    await bot.send_message(user_id, msg, parse_mode=ParseMode.MARKDOWN, reply_markup=greet_kb1)


async def generate(user_id):
    mode: int = random.randint(1, 4)
    multiplication_table = [[i * j for j in range(1, 11)] for i in range(1, 11)]
    request = ""
    correct_answer: int = 0
    this_is_division = False
    if mode == 1:
        first_denominator: int = random.randint(1, 10)
        second_denominator: int = random.randint(1, 10)
        request = "" + str(first_denominator) + " \\* " + str(second_denominator) + " = "
        correct_answer = first_denominator * second_denominator

    elif mode == 2:
        line_number: int = random.randint(1, 10)
        rand: int = random.randint(0, 9)
        first_denominator: int = multiplication_table[line_number - 1][rand]
        second_denominator: int = line_number
        request = "" + str(first_denominator) + " ÷ " + str(second_denominator) + " = "
        correct_answer = first_denominator // second_denominator
        this_is_division = True
    elif mode == 3:
        first_denominator: int = random.randint(1, 100)
        second_denominator: int = random.randint(1, first_denominator)
        request = "" + str(first_denominator) + " - " + str(second_denominator) + " = "
        correct_answer = first_denominator - second_denominator
    elif mode == 4:
        first_denominator: int = random.randint(1, 100)
        second_denominator: int = random.randint(1, 101 - first_denominator)
        request = "" + str(first_denominator) + " + " + str(second_denominator) + " = "
        correct_answer = first_denominator + second_denominator

    await answer_options(request, correct_answer, user_id, this_is_division)


async def answer_options(request: str, correct_answer, user_id, this_is_division):
    answer_position: int = random.randint(1, 5)
    list_of_option = []
    callback_array = []
    rand_answer = correct_answer
    for i in range(1, 6):
        if i == answer_position:
            list_of_option += [correct_answer]
            callback_array += ["correct_answer"]
        elif this_is_division:
            while rand_answer == correct_answer or rand_answer in list_of_option:
                rand_answer = random.randint(1, 10)
            list_of_option += [rand_answer]
            callback_array += ["answer"]
        else:
            if correct_answer - 10 < 0:
                while rand_answer == correct_answer or rand_answer in list_of_option:
                    rand_answer = random.randint(1, correct_answer + 10)
            else:
                while rand_answer == correct_answer or rand_answer in list_of_option:
                    rand_answer = random.randint(correct_answer - 10, correct_answer + 10)
            list_of_option += [rand_answer]
            callback_array += ["answer"]
    msg = text(bold('СКОЛЬКО БУДЕТ?'), request, sep='\n')
    button1 = InlineKeyboardButton(text=str(list_of_option[0]),
                                   callback_data=callback_array[0])
    button2 = InlineKeyboardButton(text=str(list_of_option[1]),
                                   callback_data=callback_array[1])
    button3 = InlineKeyboardButton(text=str(list_of_option[2]),
                                   callback_data=callback_array[2])
    button4 = InlineKeyboardButton(text=str(list_of_option[3]),
                                   callback_data=callback_array[3])
    button5 = InlineKeyboardButton(text=str(list_of_option[4]),
                                   callback_data=callback_array[4])
    button_end = InlineKeyboardButton(text='Завершить',
                                      callback_data='results')
    # keyboard = [[button1, button2, button3, button4, button5]]
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(button1, button2, button3, button4, button5, width=5)
    kb_builder.row(button_end)
    greet_kb1 = kb_builder.as_markup()
    # greet_kb1 = InlineKeyboardMarkup(inline_keyboard=keyboard)
    await bot.send_message(user_id, msg, parse_mode=ParseMode.MARKDOWN, reply_markup=greet_kb1)


if __name__ == '__main__':
    asyncio.run(start())
