import os

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv
from loguru import logger


load_dotenv()

logger.add(
        'logs/log.log',
        format='{time:yyyy-MM-dd HHH:mm:ss} {level} {message}',
        level='DEBUG',
        rotation='500 MB'
)

TOKEN = os.getenv('BOT_TOKEN')
bot = Bot(
        token=TOKEN,
        default=DefaultBotProperties(parse_mode='HTML')
)
BOT_ADMINS_IDS = list(map(int, os.getenv('BOT_ADMINS_IDS').split(',')))
DATABASE_URL = os.getenv('SQLALCHEMY_URL')
