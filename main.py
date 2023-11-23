import asyncio
import os
import random
from aiogram import Bot, types, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.filters.command import Command
from aiogram.filters import  StateFilter
from aiogram.utils.markdown import text, bold, italic
from aiogram.types import InlineKeyboardButton, BotCommand
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.state import StatesGroup, State

from dotenv import load_dotenv

load_dotenv()

bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher()
# difficulty = 0


class StateMemory(StatesGroup):
    diff0 = State()
    diff1 = State()


async def start():
    try:
        await setup_bot_commands()
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


async def setup_bot_commands():
    bot_commands: list[BotCommand] = [
        BotCommand(command="/start", description="Меню"),
        BotCommand(command="/help", description="Помощь")
    ]
    await bot.set_my_commands(commands=bot_commands, language_code='ru')


@dp.message(Command("start"))
async def process_start_command(message: types.Message):
    await start_command(message.from_user.id)


@dp.message(Command("diff_help"))
async def process_help_command(message: types.Message):
    await diff_help_command(message.from_user.id, 0)


@dp.callback_query(F.data == 'start')
async def callback_query_handler(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await start_command(callback_query.from_user.id)


@dp.callback_query(F.data.startswith("diff_help"))
async def callback_query_handler(callback_query: types.CallbackQuery, state):
    if callback_query.data == "diff_help_0":
        await state.update_data(difficulty=0)
    elif callback_query.data == "diff_help_1":
        await state.update_data(difficulty=1)
    elif callback_query.data == "diff_help_2":
        await state.update_data(difficulty=2)
    elif callback_query.data == "diff_help_ex":
        await state.update_data(difficulty=99)
    await state.set_state(StateMemory.diff0)
    user_data = await state.get_data()
    await diff_help_command(callback_query.from_user.id, user_data['difficulty'])
    await bot.answer_callback_query(callback_query.id)


@dp.callback_query(F.data.startswith("diff"))
async def callback_query_handler(callback_query: types.CallbackQuery, state):
    user_data = await state.get_data()
    await generate(callback_query.from_user.id, user_data['difficulty'])
    await bot.answer_callback_query(callback_query.id)


@dp.callback_query(F.data.endswith('answer'), StateFilter(StateMemory.diff0))
async def callback_query_handler(callback_query: types.CallbackQuery, state):
    user_data = await state.get_data()
    await bot.answer_callback_query(callback_query.id)
    if callback_query.data == 'correct_answer':
        await bot.send_message(callback_query.from_user.id, "Вы ответили верно!")
    else:
        await bot.send_message(callback_query.from_user.id, "Вы ответили неверно!")
    await generate(callback_query.from_user.id, user_data['difficulty'])


@dp.callback_query(F.data == "results")
async def callback_query_handler(callback_query: types.CallbackQuery):
    quanty = "10"
    correct = "10"
    incorrect = "10"
    msg = text(bold("РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ:"),
               bold("Всего решено: ") + quanty,
               bold("Правильных: ") + correct,
               bold("Неправильных: ") + incorrect, sep='\n')
    button_start = InlineKeyboardButton(text='Начать снова', callback_data='diff1')
    button_end = InlineKeyboardButton(text='Меню', callback_data='start')

    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(button_start, width=1)
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
               italic('Выберите сложность:'), sep='\n')
    button_1 = InlineKeyboardButton(text='Сложение и вычитание', callback_data='diff_help_0')
    button_2 = InlineKeyboardButton(text='Умножение и деление', callback_data='diff_help_1')
    button_3 = InlineKeyboardButton(text='Возведение в степень', callback_data='diff_help_2')
    button_ex = InlineKeyboardButton(text='Экзамен', callback_data='diff_help_ex')

    # keyboard = [[button_start]]
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(button_1, width=1)
    kb_builder.row(button_2)
    kb_builder.row(button_3)
    kb_builder.row(button_ex)
    greet_kb1 = kb_builder.as_markup()
    # greet_kb1 = InlineKeyboardMarkup(inline_keyboard=keyboard)
    await bot.send_message(user_id, msg, parse_mode=ParseMode.MARKDOWN, reply_markup=greet_kb1)


async def diff_help_command(user_id: any, difficulty: int):
    msg = ""
    if difficulty == 0:
        msg = text(bold("Сложение и вычитание"), italic("ОПИСАНИЕ:"),
                   bold("Сложение") + " чисел от 1 до 100",
                   bold("Вычитание") + " чисел от 1 до 100",
                   "Предлагается 5 вариантов ответа.",
                   italic("Вы готовы начать упражнения?:"), sep='\n')
    if difficulty == 1:
        msg = text(bold("Умножение и деление"), italic("ОПИСАНИЕ:"),
                   bold("Умножение") + " чисел от 1 до 10",
                   bold("Деление") + " чисел от 1 до 10",
                   "Предлагается 5 вариантов ответа.",
                   italic("Вы готовы начать упражнения?:"), sep='\n')
    if difficulty == 2:
        msg = text(bold("Возведение в степень"), italic("ОПИСАНИЕ:"),
                   bold("Умножение") + " чисел от 1 до 10",
                   bold("Деление") + " чисел от 1 до 10",
                   "Предлагается 5 вариантов ответа.",
                   italic("Вы готовы начать упражнения?:"), sep='\n')
    if difficulty == 99:
        msg = text(bold("Экзамен"), italic("ОПИСАНИЕ:"),
                   "Данный уровень сложности включает в себя все остальные уровни сложности.",
                   "Предлагается 5 вариантов ответа.",
                   italic("Вы готовы начать упражнения?:"), sep='\n')
    button_start = InlineKeyboardButton(text='Приступить', callback_data='diff')
    button_end = InlineKeyboardButton(text='Назад', callback_data='start')

    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(button_start, width=1)
    kb_builder.row(button_end)
    greet_kb1 = kb_builder.as_markup()
    await bot.send_message(user_id, msg, parse_mode=ParseMode.MARKDOWN, reply_markup=greet_kb1)


async def generate(user_id, difficulty):
    if difficulty == 99:
        mode: int = random.randint(0, 5)
    else:
        mode: int = random.randint(0, 1) + difficulty * 2
    multiplication_table = [[i * j for j in range(1, 11)] for i in range(1, 11)]
    request = ""
    correct_answer: int = 0
    this_is_division = False
    if mode == 0:
        first_denominator: int = random.randint(1, 100)
        second_denominator: int = random.randint(1, first_denominator)
        rand = random.randint(0, 3)
        if rand == 0:
            request = "" + str(second_denominator) + " + " + "x" + " = " + str(first_denominator)
        elif rand == 1:
            request = "x + " + str(second_denominator) + " = " + str(first_denominator)
        elif rand == 2:
            request = "" + str(first_denominator) + " - " + "x" + " = " + str(second_denominator)
        else:
            request = "" + str(first_denominator) + " - " + str(second_denominator) + " = ?"
        correct_answer = first_denominator - second_denominator
    elif mode == 1:
        first_denominator: int = random.randint(1, 100)
        second_denominator: int = random.randint(1, 101 - first_denominator)
        rand = random.randint(0, 1)
        if rand == 0:
            request = "x - " + str(second_denominator) + " = " + str(first_denominator)
        else:
            request = "" + str(first_denominator) + " + " + str(second_denominator) + " = ?"
        correct_answer = first_denominator + second_denominator
    elif mode == 2:
        first_denominator: int = random.randint(1, 10)
        second_denominator: int = random.randint(1, 10)
        rand = random.randint(0, 1)
        if rand == 0:
            request = "x ÷ " + str(first_denominator) + " = " + str(second_denominator)
        else:
            request = "" + str(first_denominator) + " \\* " + str(second_denominator) + " = ?"
        correct_answer = first_denominator * second_denominator
    elif mode == 3:
        line_number: int = random.randint(1, 10)
        rand: int = random.randint(0, 9)
        first_denominator: int = multiplication_table[line_number - 1][rand]
        second_denominator: int = line_number
        rand = random.randint(0, 3)
        if rand == 0:
            request = "" + str(first_denominator) + " ÷ " + "x" + " = " + str(second_denominator)
        elif rand == 1:
            request = "x \\* " + str(second_denominator) + " = " + str(first_denominator)
        elif rand == 2:
            request = "" + str(second_denominator) + " \\* " + "x" + " = " + str(first_denominator)
        else:
            request = "" + str(first_denominator) + " ÷ " + str(second_denominator) + " = ?"
        correct_answer = first_denominator // second_denominator
        this_is_division = True
    elif mode == 4:
        first_denominator: int = random.randint(1, 10)
        second_denominator: int = random.randint(0, 10)
        if first_denominator > 2:
            second_denominator: int = random.randint(0, 4)
        if first_denominator > 4:
            second_denominator: int = random.randint(0, 3)
        if first_denominator > 7:
            second_denominator: int = random.randint(0, 2)
        rand = random.randint(0, 2)
        if rand == 0:
            request = "" + str(first_denominator) + " ^ x = " + str(first_denominator ** second_denominator)
            correct_answer = second_denominator
        elif rand == 1 and first_denominator > 0:
            request = "x ^ " + str(second_denominator) + " = " + str(first_denominator ** second_denominator)
            correct_answer = first_denominator
        else:
            request = "" + str(first_denominator) + " ^ " + str(second_denominator) + " = ?"
            correct_answer = first_denominator ** second_denominator
    elif mode == 5:
        first_denominator: int = random.randint(1, 10)
        second_denominator: int = first_denominator ** 2
        request = "sqrt(" + str(second_denominator) + ") = ?"
        correct_answer = first_denominator

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
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(button1, button2, button3, button4, button5, width=5)
    kb_builder.row(button_end)
    greet_kb1 = kb_builder.as_markup()
    await bot.send_message(user_id, msg, parse_mode=ParseMode.MARKDOWN, reply_markup=greet_kb1)


if __name__ == '__main__':
    asyncio.run(start())
