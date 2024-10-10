from telegram import KeyboardButton, ReplyKeyboardMarkup

def main_kb():
    keyboard = [
        [KeyboardButton("Информация")],
        [KeyboardButton("Помощь")],
    ]
    return ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
