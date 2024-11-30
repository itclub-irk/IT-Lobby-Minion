from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.database.models import DbButton
from src.schemas import ButtonTypeEnum as BTE

admin_panel_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Посмотреть приветственное сообщение')],
        [KeyboardButton(text='Отредактировать приветственное сообщение')],
        [KeyboardButton(text='Установить количество динамических кнопок')],
        [KeyboardButton(text='Статические кнопки'),
         KeyboardButton(text='Динамические кнопки')]
    ],
    resize_keyboard=True)

working_with_buttons_kb = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton(text='Получить список всех кнопок')],
        [KeyboardButton(text='Удалить лишние кнопки'),
         KeyboardButton(text='Добавить новую кнопку')],
        [KeyboardButton(text='Вернуться в меню')]
    ]
)


async def get_buttons_kb(static: bool = False, dynamic: bool = False):
    if not (static or dynamic):
        return None
    keyboard = InlineKeyboardBuilder()

    buttons = await DbButton.get_all_buttons()
    if static:
        for kb_button in buttons:
            if kb_button.type == BTE.static:
                keyboard.button(text=kb_button.name, url=str(kb_button.url))
    if dynamic:
        for kb_button in buttons:
            if kb_button.type == BTE.dynamic:
                keyboard.button(text=kb_button.name, url=str(kb_button.url))
    if not buttons:
        return None
    keyboard.adjust(1)

    return keyboard.as_markup()


async def get_buttons_for_delete(static: bool = False, dynamic: bool = False):
    buttons = await DbButton.get_all_buttons()
    keyboard = InlineKeyboardBuilder()
    if not (static or dynamic):
        return None
    if static:
        for kb_button in buttons:
            if kb_button.type == BTE.static:
                keyboard.button(text=kb_button.name, callback_data=str(kb_button.id))
    if dynamic:
        for kb_button in buttons:
            if kb_button.type == BTE.dynamic:
                keyboard.button(text=kb_button.name, callback_data=str(kb_button.id))
    if not buttons:
        return None
    keyboard.adjust(1)
    return keyboard.as_markup()
