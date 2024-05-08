import random

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src import settings
from src.database import repository
from src.settings import logger

admin_panel_kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='Посмотреть приветственное сообщение')],
            [KeyboardButton(text='Отредактировать приветственное сообщение')],
            [KeyboardButton(text='Установить количество динамических кнопок')],
            [KeyboardButton(text='статические кнопки'),
             KeyboardButton(text='динамические кнопки')]

        ],
        resize_keyboard=True)
edit_buttons_kb = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [KeyboardButton(text='Удалить лишние кнопки'), KeyboardButton(text='Добавить новую кнопку')],
            [KeyboardButton(text='Вернуться в меню')]
        ]
)

working_with_buttons_kb = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [KeyboardButton(text='Получить список всех кнопок')],
            [KeyboardButton(text='Удалить лишние кнопки'), KeyboardButton(text='Добавить новую кнопку')],
            [KeyboardButton(text='Вернуться в меню')]
        ]
)


def static_or_dynamic_buttons_kb(buttons_config_name: str):
    logger.debug(f'{buttons_config_name=}')
    buttons_dct = repository.get_buttons(buttons_config_name)
    logger.debug(f'{buttons_dct=}')
    keyboard = InlineKeyboardBuilder()
    buttons_ids = list(buttons_dct.keys())

    for button_id in buttons_ids:
        name = buttons_dct[button_id]["name"]
        url = buttons_dct[button_id]["url"]
        keyboard.button(text=name, url=url)
    keyboard.adjust(1)
    return keyboard.as_markup()


def welcome_message_kb():
    amount_of_dynamic_buttons = repository.get_amount_of_dynamic_buttons()
    static_buttons_dct = repository.get_buttons(settings.STATIC_BUTTONS_CONFIG_NAME)
    dynamic_buttons_dct = repository.get_buttons(settings.DYNAMIC_BUTTONS_CONFIG_NAME)
    keyboard = InlineKeyboardBuilder()
    static_buttons_ids = list(static_buttons_dct.keys())
    dynamic_buttons_ids = random.sample(
            list(static_buttons_dct.keys()),
            min(amount_of_dynamic_buttons, len(dynamic_buttons_dct))
    )
    for button_id in static_buttons_ids:
        name = static_buttons_dct[button_id]["name"]
        url = static_buttons_dct[button_id]["url"]
        keyboard.button(text=name, url=url)
    for button_id in dynamic_buttons_ids:
        name = dynamic_buttons_dct[button_id]["name"]
        url = dynamic_buttons_dct[button_id]["url"]
        keyboard.button(text=name, url=url)
    keyboard.adjust(1)
    return keyboard.as_markup()


def welcome_message_kb_without_urls(buttons_config_name: str):
    buttons_dct = repository.get_buttons(buttons_config_name)
    keyboard = InlineKeyboardBuilder()
    for button_id, button_data in buttons_dct.items():
        keyboard.button(text=button_data["name"], callback_data=button_id)
    keyboard.adjust(1)
    return keyboard.as_markup()
