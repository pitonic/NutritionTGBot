from logs.logger import logger

from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters, ConversationHandler
from db import db, User
from sqlalchemy.future import select
from keyboards import main_kb
from utils.state_manager import set_current_state
from utils.message_utils import send_message
from utils.chat_filters import private_chat_only
from typing import Any

first_message = "Добро пожаловать!" # Сообщение новым пользователям
start_message = "Добро пожаловать снова!" # Сообщение пользователям
 

@private_chat_only
async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Any:
    user = update.effective_user
    if user: 
        user_id = user.id
        set_current_state(context, 0)
        async with db.session() as session:
            # Check if user already exists
            logger.debug(f"ID пользователя {user_id}")
            result = await session.execute(select(User).where(User.telegram_id == user.id))
            existing_user = result.scalar_one_or_none()
            
            if existing_user is None:
                logger.debug("Пользователь не существует")
                # User doesn't exist, create a new user
                new_user = User(telegram_id=user.id, username=user.username)
                session.add(new_user)
                text = first_message
                await session.commit()
            else:
                text = start_message

        if update.message:
            await send_message(update, context, text, reply_markup=main_kb())
        elif update.callback_query and update.effective_chat:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=text,
                reply_markup=main_kb()
            )
        
    return ConversationHandler.END 

def setup_start_handler(application):
    application.add_handler(CommandHandler("start", start_handler))
    application.add_handler(MessageHandler(
        filters.Regex("^(Главное меню)$"),
        start_handler
    ))
    logger.debug("Start handlers added");
