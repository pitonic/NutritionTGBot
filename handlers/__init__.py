from typing import Awaitable, Callable, Dict
from telegram import Update
from telegram.ext import ContextTypes

from logs.logger import logger

from .start_handler import setup_start_handler
from .menu_handler import setup_menu_handlers
from .help_handler import setup_help_handlers


all_handlers = [
    setup_start_handler,
    setup_menu_handlers,
    setup_help_handlers
]

def setup_all_handlers(app):
    for handler_setup in all_handlers:
        handler_setup(app)
