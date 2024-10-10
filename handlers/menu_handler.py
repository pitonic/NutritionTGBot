from keyboards import help_kb
from logs.logger import logger
import re
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, MessageHandler, filters
from typing import Dict, Callable, Awaitable
from utils.message_utils import send_message
from utils.chat_filters import private_chat_only

OptionHandler = Callable[[Update, ContextTypes.DEFAULT_TYPE], Awaitable[None]]

async def information(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = "Информация"
    await send_message(update, context, text) 

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = "Выберите опцию: "
    await send_message(update, context, text, reply_markup=help_kb())

menu_options: Dict[str, OptionHandler] = {
    "Информация": information,
    "Помощь": help
}

@private_chat_only
async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.message.text:
        logger.warning("Получен update без сообщения или текста в menu_handler")
        return

    option = update.message.text
    handler = menu_options.get(option)
    
    if handler:
        await handler(update, context)
    else:
        await update.message.reply_text(f"Неизвестная опция: {option}")

def setup_menu_handlers(application):
    main_menu_filter = filters.Regex('^(' + '|'.join(map(re.escape, menu_options.keys())) + ')$')
    application.add_handler(MessageHandler(main_menu_filter & ~filters.COMMAND, menu_handler))
    application.add_handler(CommandHandler("help", help))
    logger.debug("Добавлены menu handlers")


