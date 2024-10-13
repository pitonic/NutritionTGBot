from logs.logger import logger
import re
from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters
from typing import Dict, Callable, Awaitable
from utils.message_utils import send_message
from utils.chat_filters import private_chat_only
from keyboards.data_source_kb import receipts_kb

OptionHandler = Callable[[Update, ContextTypes.DEFAULT_TYPE], Awaitable[None]]

async def data_source(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = "Выберите опцию: "
    await send_message(update, context, text, reply_markup=receipts_kb()) 

async def how_to_receipts(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = "Как добавлять чеки"
    await send_message(update, context, text, reply_markup=receipts_kb())

async def receipts_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = "Список чеков"
    await send_message(update, context, text, reply_markup=receipts_kb())

async def purchased_p_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = "Список купленных продуктов"
    await send_message(update, context, text, reply_markup=receipts_kb())

async def unrecognized_p_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = "Список нераспознанных продуктов"
    await send_message(update, context, text, reply_markup=receipts_kb())

menu_options: Dict[str, OptionHandler] = {
    "Источники данных": data_source,
    "Как добавлять чеки": how_to_receipts,
    "Список чеков": receipts_list,
    "Список купленных продуктов": purchased_p_list,
    "Список нераспознанных продуктов": unrecognized_p_list,
}

@private_chat_only
async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.message.text:
        logger.warning("Получен update без сообщения или текста в menu_handler")
        return

    option = update.message.text
    handler = menu_options.get(option)
    
    if handler:
        await handler(update, context)
    else:
        await update.message.reply_text(f"Неизвестная опция: {option}")

def setup_data_source_handlers(application):
    filter = filters.Regex('^(' + '|'.join(map(re.escape, menu_options.keys())) + ')$')
    application.add_handler(MessageHandler(filter & ~filters.COMMAND, handler))
    logger.debug("Добавлены menu handlers")


