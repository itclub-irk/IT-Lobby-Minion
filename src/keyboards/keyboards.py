import random

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.database import repository

admin_panel_kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='Посмотреть приветственное сообщение')],
            [KeyboardButton(text='Отредактировать приветственное сообщение')],
            [KeyboardButton(text='Получить список всех кнопок')],
            [KeyboardButton(text='Отредактировать кнопки')]

        ],
        resize_keyboard=True)
edit_buttons_kb = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [KeyboardButton(text='Удалить лишние кнопки'), KeyboardButton(text='Добавить новую кнопку')],
            [KeyboardButton(text='Вернуться в меню')]
        ]
)


def welcome_message_kb(amount_of_buttons: int = 3):
    buttons_dct = repository.get_buttons()
    keyboard = InlineKeyboardBuilder()
    button_ids = random.sample(list(buttons_dct.keys()), min(amount_of_buttons, len(buttons_dct)))
    for button_id in button_ids:
        name = buttons_dct[button_id]["name"]
        url = buttons_dct[button_id]["url"]
        keyboard.button(text=name, url=url)
    keyboard.adjust(1)
    return keyboard.as_markup()


def welcome_message_kb_without_urls():
    buttons_dct = repository.get_buttons()
    keyboard = InlineKeyboardBuilder()
    for button_id, button_data in buttons_dct.items():
        keyboard.button(text=button_data["name"], callback_data=button_id)
    keyboard.adjust(1)
    return keyboard.as_markup()
