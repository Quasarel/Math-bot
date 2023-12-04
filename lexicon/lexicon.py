from aiogram.utils.markdown import text, bold, italic

LEXICON: dict[str, str] = {
    'settings': text(bold('Выберите, какой таймаут будет использоваться в тренажере')),
    '5_sec': '5 сек',
    '10_sec': '10 сек',
    '15_sec': '15 сек',
    '30_sec': '30 сек',
    'menu': 'Меню',
    'settings_success': "Настройки успешно установлены\nЧто делать дальше?",
    'correct_answer': "✅ Вы ответили верно!",
    'incorrect_answer': "❌ Вы ответили неверно!",
    'times_out': "⏱ Время вышло",
    'results': text(bold("РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ:"),
                    bold("Всего решено: ") + "%4 из %3",
                    bold("Правильных: ") + "%1",
                    bold("Неправильных: ") + "%2", sep='\n'),
    'what_to_do': 'Что делать дальше?',
    'main_menu': text(bold('      ГЛАВНОЕ МЕНЮ'),
                      italic('Выберите сложность:'), sep='\n'),
    'diff_0': 'Сложение и вычитание',
    'diff_1': 'Умножение и деление',
    'diff_2': 'Возведение в степень',
    'diff_ex': 'Экзамен',
    'help': text(bold("Помощь"),
                 bold("/start") + " – запуск главного меню и выбор уровня сложности.",
                 bold("/settings") + " – настройка ограничения по времени.", sep='\n'),
    'begin': 'Приступить',
    'back': 'Назад',
    'diff_0_help': text(bold("Сложение и вычитание"), italic("ОПИСАНИЕ:"),
                        bold("Сложение") + " чисел от 1 до 100",
                        bold("Вычитание") + " чисел от 1 до 100",
                        "Предлагается 5 вариантов ответа.",
                        italic("Вы готовы начать упражнения?:"), sep='\n'),
    'diff_1_help': text(bold("Умножение и деление"), italic("ОПИСАНИЕ:"),
                        bold("Умножение") + " чисел от 1 до 10",
                        bold("Деление") + " чисел от 1 до 10",
                        "Предлагается 5 вариантов ответа.",
                        italic("Вы готовы начать упражнения?:"), sep='\n'),
    'diff_2_help': text(bold("Возведение в степень"), italic("ОПИСАНИЕ:"),
                        bold("Возведение") + " чисел от 1 до 10 " + bold("в степень") + " от 0 до 10",
                        bold("Извлечение квадратного корня") + " чисел от 1 до 100",
                        "Предлагается 5 вариантов ответа.",
                        italic("Вы готовы начать упражнения?:"), sep='\n'),
    'diff_ex_help': text(bold("Экзамен"), italic("ОПИСАНИЕ:"),
                         "Данный уровень сложности включает в себя все остальные уровни сложности.",
                         "Предлагается 5 вариантов ответа.",
                         italic("Вы готовы начать упражнения?:"), sep='\n'),
    'what_is': text(bold('СКОЛЬКО БУДЕТ'), "%1", sep='\n'),
    'end': 'Завершить',
    'time_left': "Поторопитесь, у вас %1 секунд",
    'try_again': 'Начать снова',
}

LEXICON_COMMANDS: dict[str, str] = {
    '/start': 'Меню',
    '/help': 'Помощь',
    '/settings': 'Настройки'
}
