from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.database import repository
from src.keyboards import welcome_message_kb
from src.settings import BOT_ADMIN_ID
from src.states import FSM_admin_panel

router = Router()


@router.message(F.text == 'Посмотреть приветственное сообщение')
async def get_welcome_message(message: Message, state: FSMContext):
    if message.from_user.id != BOT_ADMIN_ID:
        await message.answer('Только админ может делать это')
        await message.delete()
        return
    welcome_message = repository.get_welcome_message_text(message)
    if welcome_message:
        await message.answer(
                text=welcome_message,
                reply_markup=welcome_message_kb(),
        )
    else:
        await message.answer('Приветственное сообщение не установлено')
        await message.answer('Используй\n\n"Отредактировать приветственное сообщение"')
    await message.delete()
    await state.clear()


@router.message(F.text == 'Отредактировать приветственное сообщение')
async def edit_welcome_message(message: Message, state: FSMContext):
    if message.from_user.id != BOT_ADMIN_ID:
        await message.answer('Только админ может делать это')
        await message.delete()
        return
    await message.answer(
            'Отправь мне текст для сообщения, можешь использовать встроенное форматирование от ТГ'
    )
    await message.delete()
    await state.set_state(FSM_admin_panel.get_message)


@router.message(FSM_admin_panel.get_message)
async def get_message(message: Message, state: FSMContext):
    repository.set_welcome_message_text(message.html_text)
    await message.answer('Текст для приветственного сообщения установлен')
    await state.clear()


@router.message(F.text == 'Установить количество динамических кнопок')
async def send_amount_of_buttons(message: Message, state: FSMContext):
    await message.answer('Пришлите мне количество динамических кнопок (числом)')
    await state.set_state(FSM_admin_panel.get_amount_of_dynamic_buttons)


@router.message(FSM_admin_panel.get_amount_of_dynamic_buttons)
async def get_amount_of_dynamic_buttons(message: Message, state: FSMContext):
    try:
        amount = int(message.text)
    except ValueError:
        await message.answer('Неверный формат')
        await message.answer('Пришлите мне количество динамических кнопок (числом)')
        return
    repository.set_amount_of_dynamic_buttons(amount)
    await message.answer(f'Установлено <b>{amount}</b> динамических кнопок для сообщения')
    await state.clear()
