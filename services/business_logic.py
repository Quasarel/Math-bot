import asyncio
import random
from aiogram import types
from aiogram.types import Message
from aiogram.enums import ParseMode
from database import database as db
from database.db_map import Settings
from aiogram.fsm.state import StatesGroup, State
from keyboard.keyboard import create_results_kb, create_answer_option_kb

from lexicon.lexicon import LEXICON

# question_count = 10
user_dict: dict[int, dict[str, int]] = {}


class StateMemory(StatesGroup):
    diff0 = State()


async def display_results(message: Message):
    messages = user_dict[message.chat.id]
    quantity = len(user_dict[message.chat.id])
    correct = 0
    incorrect = 0
    for v in messages.values():
        if v == 1:
            correct += 1
        elif v == 2:
            incorrect += 1
    if user_dict[message.chat.id][str(message.message_id)] == 0:
        list_answer = message.md_text.replace("\\=", "=").replace("\\+", "+").replace("\\-", "-").split("\n")
        list_answer[2] = LEXICON['times_up']
        await message.edit_text(text="\n".join(list_answer), parse_mode=ParseMode.MARKDOWN)
    user_dict[message.chat.id] = {}
    msg = LEXICON['results'] \
        .replace("%4", str(correct + incorrect)) \
        .replace("%3", str(quantity)) \
        .replace("%1", str(correct)) \
        .replace("%2", str(incorrect))

    results_kb = create_results_kb()

    await message.answer(msg, parse_mode=ParseMode.MARKDOWN)
    session = db.Session()
    settings = session.get(Settings, message.chat.id)
    question_count = 10
    if settings:
        question_count = settings.question_count
    session.close()
    if correct + incorrect > 0 and incorrect == 0:
        await message.answer("😎", reply_markup=types.ReplyKeyboardRemove())
    elif correct + incorrect == 0:
        await message.answer("😴", reply_markup=types.ReplyKeyboardRemove())
    elif incorrect * question_count / (correct + incorrect) < 0.3 * question_count:
        await message.answer("😄", reply_markup=types.ReplyKeyboardRemove())
    elif incorrect * question_count / (correct + incorrect) <= 0.5 * question_count:
        await message.answer("😐", reply_markup=types.ReplyKeyboardRemove())
    elif incorrect * question_count / (correct + incorrect) < 0.7 * question_count:
        await message.answer("☹", reply_markup=types.ReplyKeyboardRemove())
    elif incorrect * question_count / (correct + incorrect) == question_count:
        await message.answer("🤨", reply_markup=types.ReplyKeyboardRemove())
    else:
        await message.answer("😫", reply_markup=types.ReplyKeyboardRemove())
    await message.answer(LEXICON['what_to_do'], parse_mode=ParseMode.MARKDOWN, reply_markup=results_kb)


async def generate(message: Message, chapter, difficulty):
    if difficulty == 99:
        if chapter == 99:
            chapter: int = random.randint(0, 2)
        mode = 0
        if chapter == 0:
            mode: int = random.randint(0, 5)
        elif chapter == 1:
            mode: int = random.randint(0, 3)
        elif chapter == 2:
            mode: int = random.randint(0, 1)
    else:
        mode: int = 1  # random.randint(0, 1) + difficulty * 2
    multiplication_table = [[i * j for j in range(1, 11)] for i in range(1, 11)]
    # angle = ["0", "π/6", "π/4", "π/3", "π/2", "π", "3π/2", "2π"]
    angle = ["0", "π/6", "π/4", "π/3", "π/2", "2π/3", "3π/4", "5π/6", "π",
             "7π/6", "5π/4", "4π/3", "3π/2", "5π/3", "7π/4", "11π/6", "2π"]
    # sin_value = ["0", "1/2", "√2/2", "√3/2", "1", "0", "-1", "0"]
    sin_value = ["0", "1/2", "√2/2", "√3/2", "1", "√3/2", "√2/2", "1/2", "0",
                 "-1/2", "-√2/2", "-√3/2", "-1", "-√3/2", "-√2/2", "-1/2", "0"]
    # cos_value = ["1", "√3/2", "√2/2", "1/2", "0", "-1", "0", "1"]
    cos_value = ["1", "√3/2", "√2/2", "1/2", "0", "-1/2", "-√2/2", "-√3/2", "-1",
                 "-√3/2", "-√2/2", "-1/2", "0", "1/2", "√2/2", "√3/2", "1"]
    # tg_value = ["0", "√3/3", "1", "√3", "не опр.", "0", "не опр.", "0"]
    tg_value = ["0", "√3/3", "1", "√3", "не опр.", "-√3", "-1", "-√3/3",
                "0", "√3/3", "1", "√3", "не опр.", "-√3", "-1", "-√3/3", "0"]
    # ctg_value = ["не опр.", "√3", "1", "√3/3", "0", "не опр.", "0", "не опр."]
    ctg_value = ["не опр.", "-√3", "-1", "-√3/3", "0", "√3/3", "1", "√3",
                 "не опр.", "-√3", "-1", "-√3/3", "0", "√3/3", "1", "√3", "не опр."]
    angle = ["0", "π/6", "π/4", "π/3", "π/2", "2π/3", "3π/4", "5π/6", "π",
             "7π/6", "5π/4", "4π/3", "3π/2", "5π/3", "7π/4", "11π/6", "2π"]
    derivative = ["C", "x", "√x", "a^x", "e^x", "lnx", "sin(x)", "cos(x)"]
    derivative_value = ["0", "1", "1/2√x", "a^(x)lna", "e^x", "1/x", "cos(x)", "-sin(x)"]
    request = ""
    correct_answer = 0
    this_is_division = False
    if chapter == 0:
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
            elif rand == 1 and second_denominator > 0:
                request = "x ^ " + str(second_denominator) + " = " + str(first_denominator ** second_denominator)
                correct_answer = first_denominator
            else:
                request = "" + str(first_denominator) + " ^ " + str(second_denominator) + " = ?"
                correct_answer = first_denominator ** second_denominator
        elif mode == 5:
            first_denominator: int = random.randint(1, 10)
            second_denominator: int = first_denominator ** 2
            request = "√" + str(second_denominator) + " = ?"
            correct_answer = first_denominator
    elif chapter == 1:
        if mode == 0:
            rand = random.randint(0, len(angle)-1)
            first_denominator: str = angle[rand]
            second_denominator: str = sin_value[rand]
            request = "sin(" + str(first_denominator) + ") = ?"
            correct_answer = second_denominator
        elif mode == 1:
            rand = random.randint(0, len(angle)-1)
            first_denominator: str = angle[rand]
            second_denominator: str = cos_value[rand]
            request = "cos(" + str(first_denominator) + ") = ?"
            correct_answer = second_denominator
        if mode == 2:
            rand = random.randint(0, len(angle)-1)
            first_denominator: str = angle[rand]
            second_denominator: str = tg_value[rand]
            request = "tg(" + str(first_denominator) + ") = ?"
            correct_answer = second_denominator
        if mode == 3:
            rand = random.randint(0, len(angle)-1)
            first_denominator: str = angle[rand]
            second_denominator: str = ctg_value[rand]
            request = "ctg(" + str(first_denominator) + ") = ?"
            correct_answer = second_denominator
    elif chapter == 2:
        if mode == 0:
            rand = random.randint(0, len(derivative)-1)
            first_denominator: str = derivative[rand]
            second_denominator: str = derivative_value[rand]
            request = "f'(" + str(first_denominator) + ") = ?"
            correct_answer = second_denominator
        if mode == 1:
            rand = random.randint(0, len(derivative) - 1)
            first_denominator: str = derivative[rand]
            second_denominator: str = derivative_value[rand]
            request = "F'(" + str(second_denominator) + ") = ? + C"
            correct_answer = first_denominator
    await answer_options(request, correct_answer, message, this_is_division, chapter, difficulty)


async def answer_options(request: str, correct_answer, message, this_is_division, chapter, difficulty):
    user_id = message.chat.id
    session = db.Session()
    settings = session.get(Settings, user_id)
    timeout = 5
    question_count = 10
    # angle = ["0", "pi/6", "pi/4", "pi/3", "pi/2", "pi", "3\\*pi/2", "2\\*pi"]
    trigonometric_value = ["0", "1/2", "√2/2", "√3/2", "1", "-√3/2", "-√2/2", "-1/2",
                           "-1", "√3/3", "√3", "-√3/3", "-√3", "не опр."]
    derivative_value = ["0", "1", "1/2√x", "a^(x)lna", "e^x", "1/x", "cos(x)", "-sin(x)",
                        "C", "x", "√x", "a^x", "e^x", "lnx", "sin(x)", "cos(x)"]
    if settings:
        timeout = settings.timer_limit
        question_count = settings.question_count
    session.close()
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
            callback_array += ["answer_" + str(correct_answer)]
        else:
            if chapter == 0:
                if correct_answer - 10 < 0:
                    while rand_answer == correct_answer or rand_answer in list_of_option:
                        rand_answer = random.randint(1, correct_answer + 10)
                else:
                    while rand_answer == correct_answer or rand_answer in list_of_option:
                        rand_answer = random.randint(correct_answer - 10, correct_answer + 10)
            elif chapter == 1:
                while rand_answer == correct_answer or rand_answer in list_of_option:
                    rand_answer = trigonometric_value[random.randint(1, len(trigonometric_value)-1)]
            else:
                while rand_answer == correct_answer or rand_answer in list_of_option:
                    rand_answer = derivative_value[random.randint(1, len(derivative_value)-1)]
            list_of_option += [rand_answer]
            callback_array += ["answer_" + str(correct_answer)]
    msg = LEXICON['what_is'].replace("%1", request)
    answer_option_kb = create_answer_option_kb(list_of_option, callback_array)
    timer_message = LEXICON['time_left'].replace("%1", str(timeout))
    message = await message.answer(msg + "\n" + timer_message,
                                   parse_mode=ParseMode.MARKDOWN, reply_markup=answer_option_kb)
    if message.chat.id not in user_dict:
        user_dict[message.chat.id] = {}
    user_dict[message.chat.id][str(message.message_id)] = 0
    while timeout != 0:
        await asyncio.sleep(1)
        timeout = timeout - 1
        timer_message = LEXICON['time_left'].replace("%1", str(timeout))
        if user_dict[message.chat.id] and user_dict[message.chat.id][str(message.message_id)] == 0:
            await message.edit_text(text=msg + "\n" + timer_message,
                                    parse_mode=ParseMode.MARKDOWN, reply_markup=message.reply_markup)
        else:
            break

    if user_dict[message.chat.id] and user_dict[message.chat.id][str(message.message_id)] == 0:
        timer_message = LEXICON['times_up']
        await message.edit_text(text=msg + "\n" + timer_message, parse_mode=ParseMode.MARKDOWN)
        if len(user_dict[message.chat.id]) >= question_count:
            await display_results(message)
        else:
            await generate(message, chapter, difficulty)
