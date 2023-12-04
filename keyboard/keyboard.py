from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import LEXICON


def create_start_kb() -> InlineKeyboardMarkup:
    button_1 = InlineKeyboardButton(text=LEXICON['diff_0'], callback_data='diff_help_0')
    button_2 = InlineKeyboardButton(text=LEXICON['diff_1'], callback_data='diff_help_1')
    button_3 = InlineKeyboardButton(text=LEXICON['diff_2'], callback_data='diff_help_2')
    button_ex = InlineKeyboardButton(text=LEXICON['diff_ex'], callback_data='diff_help_ex')

    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(button_1, width=1)
    kb_builder.row(button_2)
    kb_builder.row(button_3)
    kb_builder.row(button_ex)
    return kb_builder.as_markup()


def create_help_kb() -> InlineKeyboardMarkup:
    button_start = InlineKeyboardButton(text=LEXICON['begin'], callback_data='diff')
    button_end = InlineKeyboardButton(text=LEXICON['back'], callback_data='start')
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(button_start, width=1)
    kb_builder.row(button_end)
    return kb_builder.as_markup()


def create_settings_kb() -> InlineKeyboardMarkup:
    button_5 = InlineKeyboardButton(text=LEXICON['5_sec'],  callback_data='settings_5')
    button_10 = InlineKeyboardButton(text=LEXICON['10_sec'], callback_data='settings_10')
    button_15 = InlineKeyboardButton(text=LEXICON['15_sec'], callback_data='settings_15')
    button_30 = InlineKeyboardButton(text=LEXICON['30_sec'], callback_data='settings_30')

    keyboard = [[button_5, button_10, button_15, button_30]]

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def create_settings_success() -> InlineKeyboardMarkup:
    button_end = InlineKeyboardButton(text=LEXICON['menu'], callback_data='start')

    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(button_end, width=1)
    return kb_builder.as_markup()


def create_results_kb() -> InlineKeyboardMarkup:
    button_start = InlineKeyboardButton(text=LEXICON['try_again'], callback_data='diff')
    button_end = InlineKeyboardButton(text=LEXICON['menu'], callback_data='start')

    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(button_start, width=1)
    kb_builder.row(button_end)
    return kb_builder.as_markup()


def create_answer_option_kb(list_of_option, callback_array) -> InlineKeyboardMarkup:
    button1 = InlineKeyboardButton(text=str(list_of_option[0]), callback_data=callback_array[0])
    button2 = InlineKeyboardButton(text=str(list_of_option[1]), callback_data=callback_array[1])
    button3 = InlineKeyboardButton(text=str(list_of_option[2]), callback_data=callback_array[2])
    button4 = InlineKeyboardButton(text=str(list_of_option[3]), callback_data=callback_array[3])
    button5 = InlineKeyboardButton(text=str(list_of_option[4]), callback_data=callback_array[4])
    button_end = InlineKeyboardButton(text=LEXICON['end'], callback_data='results')
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(button1, button2, button3, button4, button5, width=5)
    kb_builder.row(button_end)
    return kb_builder.as_markup()
