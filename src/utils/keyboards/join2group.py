from aiogram.utils.keyboard import InlineKeyboardBuilder
from random import sample
from src.schemas import ButtonTypeEnum as BTE
from src.database.models import DbButton, DbSettings


async def welcome_keyboard():
    amount_dynamic_buttons = (await DbSettings.get_settings()).dynamic_button_count

    keyboard = InlineKeyboardBuilder()

    buttons = await DbButton.get_all_buttons()

    dynamic_buttons = []
    for kb_button in buttons:
        if kb_button.type == BTE.static:
            keyboard.button(text=kb_button.name, url=str(kb_button.url))
        else:
            dynamic_buttons.append(kb_button)
    for kb_button in sample(dynamic_buttons, min(amount_dynamic_buttons, len(dynamic_buttons))):
        keyboard.button(text=kb_button.name, url=str(kb_button.url))
    if not buttons:
        return None
    keyboard.adjust(1)

    return keyboard.as_markup()
