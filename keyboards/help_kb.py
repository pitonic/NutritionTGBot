from telegram import KeyboardButton, ReplyKeyboardMarkup

def help_kb():
    keyboard = [
            [KeyboardButton("Часто задаваемые вопросы")],
        [KeyboardButton("Вторая кнопка")],
        [KeyboardButton("Главное меню")],
    ]
    return ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
