from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.database.models import DbSettings
from src.states.admin import FSM_admin_panel
from src.utils.filters import AdminRoleFilter
from src.utils.keyboards.join2group import welcome_keyboard
from src.utils.welcome_message import configure_welcome_message

router = Router()


@router.message(F.text == 'Посмотреть приветственное сообщение',  AdminRoleFilter())
async def get_welcome_message(message: Message, state: FSMContext):
    welcome_message = await configure_welcome_message(
        user_full_name=message.from_user.full_name,
        username=message.from_user.username,
        user_id=message.from_user.id,
    )
    if welcome_message:
        await message.answer(
            text=welcome_message,
            reply_markup=(await welcome_keyboard()),
        )
    await message.delete()
    await state.clear()


@router.message(F.text == 'Отредактировать приветственное сообщение',  AdminRoleFilter())
async def edit_welcome_message(message: Message, state: FSMContext):
    await message.answer(
        'Отправь мне текст для сообщения, можешь использовать встроенное форматирование от ТГ\n\n'
        'Чтобы я понял, куда поставить имя пользователя и username используй:\n\n'
        '<b>{{NAME}}</b> и <b>{{USERNAME}}</b>',
    )
    await message.delete()
    await state.set_state(FSM_admin_panel.get_message)


@router.message(FSM_admin_panel.get_message,  AdminRoleFilter())
async def get_message(message: Message, state: FSMContext):
    await DbSettings.set_settings(welcome_message=message.html_text)
    await message.answer('Текст для приветственного сообщения установлен')
    await state.clear()


@router.message(F.text == 'Установить количество динамических кнопок',  AdminRoleFilter())
async def send_amount_of_buttons(message: Message, state: FSMContext):
    await message.answer('Пришлите мне количество динамических кнопок (числом)')
    await state.set_state(FSM_admin_panel.get_amount_of_dynamic_buttons)


@router.message(FSM_admin_panel.get_amount_of_dynamic_buttons,  AdminRoleFilter())
async def get_amount_of_dynamic_buttons(message: Message, state: FSMContext):
    try:
        amount = int(message.text)
    except ValueError:
        await message.answer('Неверный формат')
        await message.answer('Пришлите мне количество динамических кнопок (числом)')
        return
    await DbSettings.set_settings(dynamic_button_count=amount)
    await message.answer(f'Установлено <b>{amount}</b> динамических кнопок для сообщения')
    await state.clear()
