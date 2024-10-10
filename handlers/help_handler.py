from logs.logger import logger
import re
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, MessageHandler, filters
from typing import Dict, Callable, Awaitable
from utils.message_utils import send_message
from utils.chat_filters import private_chat_only

OptionHandler = Callable[[Update, ContextTypes.DEFAULT_TYPE], Awaitable[None]]

async def faq(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = "Часто задаваемые вопросы..."
    await send_message(update, context, text) 

async def option_2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = "Выбрана опция 2"
    await send_message(update, context, text)

menu_options: Dict[str, OptionHandler] = {
    "Часто задаваемые вопросы": faq,
    "Вторая кнопка": option_2
}

@private_chat_only
async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.message.text:
        logger.warning("Получен update без сообщения или текста в menu_handler")
        return

    option = update.message.text
    handler = menu_options.get(option)
    
    if handler:
        await handler(update, context)
    else:
        await update.message.reply_text(f"Неизвестная опция: {option}")

def setup_help_handlers(application):
    help_filter = filters.Regex('^(' + '|'.join(map(re.escape, menu_options.keys())) + ')$')
    application.add_handler(MessageHandler(help_filter & ~filters.COMMAND, help_handler))
    application.add_handler(CommandHandler("help", help))
    logger.debug("Добавлены help handlers")


