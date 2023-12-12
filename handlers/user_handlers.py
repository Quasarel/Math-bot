from aiogram import types, Router, F
from aiogram.enums import ParseMode
from aiogram.types import Message, CallbackQuery
from database import database as db
from database.db_map import Settings
from aiogram.filters.command import Command
from services.business_logic import user_dict, StateMemory, generate, display_results
from keyboard.keyboard import (create_start_kb, create_help_kb, create_help_0_kb, create_help_1_kb, create_help_2_kb,
                               create_help_ex_kb, create_settings_kb, create_settings_success, create_settings2_kb)

from lexicon.lexicon import LEXICON

router = Router()


@router.message(Command("start"))
async def process_start_command(message: Message):
    await start_command(message)


@router.callback_query(F.data == 'start')
async def callback_query_handler(callback_query: CallbackQuery):
    await callback_query.answer()
    await start_command(callback_query.message)


async def start_command(message: Message):
    user_dict[message.chat.id] = {}
    msg = LEXICON['main_menu']
    start_kb = create_start_kb()
    await message.answer(msg, parse_mode=ParseMode.MARKDOWN, reply_markup=start_kb)


@router.message(Command("help"))
async def process_help_command(message: Message):
    msg = LEXICON['help']
    help_kb = create_help_kb()
    await message.answer(msg, parse_mode=ParseMode.MARKDOWN, reply_markup=help_kb)


@router.message(Command("settings"))
async def process_start_command(message: Message):
    msg = LEXICON['settings']
    settings_kb = create_settings_kb()
    await message.answer(msg, parse_mode=ParseMode.MARKDOWN, reply_markup=settings_kb)


@router.callback_query(F.data.startswith('settings'))
async def callback_query_handler(callback_query: CallbackQuery):
    await callback_query.answer()
    with db.Session() as session:
        settings = session.get(Settings, callback_query.message.chat.id)
        if settings:
            settings.timer_limit = int(callback_query.data.replace("settings_", ""))
        else:
            session.add(Settings(tg_id=callback_query.message.chat.id,
                                 timer_limit=int(callback_query.data.replace("settings_", "")), question_count=10))
        session.commit()
        session.close()
    settings2 = create_settings2_kb()
    await callback_query.message.answer(LEXICON['settings2'], parse_mode=ParseMode.MARKDOWN,
                                        reply_markup=settings2)


@router.callback_query(F.data.startswith('question'))
async def callback_query_handler(callback_query: CallbackQuery):
    await callback_query.answer()
    with db.Session() as session:
        settings = session.get(Settings, callback_query.message.chat.id)
        settings.question_count = int(callback_query.data.replace("question_", ""))
        session.commit()
        session.close()
    settings_success = create_settings_success()
    await callback_query.message.answer(LEXICON['settings_success'], parse_mode=ParseMode.MARKDOWN,
                                        reply_markup=settings_success)


@router.callback_query(F.data.startswith("diff_help"))
async def callback_query_handler(callback_query: CallbackQuery, state):
    msg = ""
    diff_help_kb = create_help_0_kb()
    if callback_query.data == "diff_help_0":
        msg = LEXICON['diff_0_help']
        await state.update_data(chapter=0)
        diff_help_kb = create_help_0_kb()
    elif callback_query.data == "diff_help_1":
        msg = LEXICON['diff_1_help']
        await state.update_data(chapter=1)
        diff_help_kb = create_help_1_kb()
    elif callback_query.data == "diff_help_2":
        msg = LEXICON['diff_2_help']
        await state.update_data(chapter=2)
        diff_help_kb = create_help_2_kb()
    elif callback_query.data == "diff_help_ex":
        msg = LEXICON['diff_ex_help']
        await state.update_data(chapter=99)
        diff_help_kb = create_help_ex_kb()
    await callback_query.answer()
    await callback_query.message.answer(msg, parse_mode=ParseMode.MARKDOWN, reply_markup=diff_help_kb)


@router.callback_query(F.data.startswith("diff"))
async def callback_query_handler(callback_query: types.CallbackQuery, state):
    user_data = await state.get_data()
    if user_data['chapter'] == 0:
        if callback_query.data == "diff_0":
            await state.update_data(difficulty=0)
        elif callback_query.data == "diff_1":
            await state.update_data(difficulty=1)
        elif callback_query.data == "diff_2":
            await state.update_data(difficulty=2)
        elif callback_query.data == "diff_ex":
            await state.update_data(difficulty=99)
    elif user_data['chapter'] == 1:
        if callback_query.data == "diff_0":
            await state.update_data(difficulty=0)
        if callback_query.data == "diff_1":
            await state.update_data(difficulty=1)
        elif callback_query.data == "diff_ex":
            await state.update_data(difficulty=99)
    elif user_data['chapter'] == 2:
        if callback_query.data == "diff_0":
            await state.update_data(difficulty=0)
    else:
        await state.update_data(difficulty=99)
    await state.set_state(StateMemory.diff0)
    user_data = await state.get_data()
    await callback_query.answer()
    await generate(callback_query.message, user_data['chapter'], user_data['difficulty'])


@router.callback_query(F.data == 'correct_answer')
async def callback_query_handler(callback_query: types.CallbackQuery, state):
    session = db.Session()
    settings = session.get(Settings, callback_query.message.chat.id)
    question_count = 10
    if settings:
        question_count = settings.question_count
    session.close()
    user_data = await state.get_data()
    if callback_query.message.chat.id not in user_dict:
        user_dict[callback_query.message.chat.id] = {}
    user_dict[callback_query.message.chat.id][str(callback_query.message.message_id)] = 1
    list_answer = callback_query.message.md_text.replace("\\)", ")").replace("\\(", "(")\
        .replace("\\=", "=").replace("\\+", "+").replace("\\-", "-").split("\n")
    list_answer[2] = LEXICON['correct_answer']
    await callback_query.message.edit_text(text="\n".join(list_answer), parse_mode=ParseMode.MARKDOWN)
    await callback_query.answer()
    if len(user_dict[callback_query.message.chat.id]) >= question_count:
        await display_results(callback_query.message)
    else:
        await generate(callback_query.message, user_data['chapter'], user_data['difficulty'])


@router.callback_query(F.data.startswith('answer'))
async def callback_query_handler(callback_query: types.CallbackQuery, state):
    session = db.Session()
    settings = session.get(Settings, callback_query.message.chat.id)
    question_count = 10
    if settings:
        question_count = settings.question_count
    session.close()
    user_data = await state.get_data()
    if callback_query.message.chat.id not in user_dict:
        user_dict[callback_query.message.chat.id] = {}
    user_dict[callback_query.message.chat.id][str(callback_query.message.message_id)] = 2
    # list_answer = callback_query.message.text.replace("*", "\\*").split("\n")
    list_answer = callback_query.message.md_text.replace("\\)", ")").replace("\\(", "(")\
        .replace("\\=", "=").replace("\\+", "+").replace("\\-", "-").split("\n")
    list_answer[2] = LEXICON['incorrect_answer']
    correct_answer = callback_query.data.split("_")[1]
    list_answer.append(list_answer[1].replace("?", correct_answer).replace("x", correct_answer))
    await callback_query.message.edit_text(text="\n".join(list_answer), parse_mode=ParseMode.MARKDOWN)
    await callback_query.answer()
    if len(user_dict[callback_query.message.chat.id]) >= question_count:
        await display_results(callback_query.message)
    else:
        await generate(callback_query.message, user_data['chapter'], user_data['difficulty'])


@router.callback_query(F.data == "results")
async def callback_query_handler(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await display_results(callback_query.message)
