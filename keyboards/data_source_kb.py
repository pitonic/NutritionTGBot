from telegram import KeyboardButton, ReplyKeyboardMarkup

def receipts_kb():
    keyboard = [
        [KeyboardButton("Как добавлять чеки"), KeyboardButton("Список чеков")],
        [KeyboardButton("Список купленных продуктов")],
        [KeyboardButton("Список нераспознанных продуктов")],
        [KeyboardButton("Главное меню")],
    ]
    return ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
