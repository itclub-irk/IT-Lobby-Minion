import os

from aiogram import Bot
from loguru import logger
from dotenv import load_dotenv


load_dotenv()

logger.add(
        'logs/log.log',
    format='{time:yyyy-MM-dd HHH:mm:ss} {level} {message}',
    level='DEBUG',
    rotation='50 MB'
)

bot = Bot(
        token=os.getenv('BOT_TOKEN'),
        parse_mode='HTML'
)
BOT_ADMIN_ID = int(os.getenv('BOT_ADMIN_ID'))
