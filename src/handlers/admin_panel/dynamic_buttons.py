import asyncio

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from src.config import logger
from src.database.models import DbButton
from src.schemas import ButtonTypeEnum as BTE
from src.states.admin import FSM_DynamicButtons
from src.utils.filters import AdminRoleFilter
from src.utils.keyboards.admin import (
    get_buttons_for_delete, get_buttons_kb,
    working_with_buttons_kb,
)
from src.utils.keyboards.join2group import welcome_keyboard

router = Router()


@router.message(F.text == 'Динамические кнопки', AdminRoleFilter())
@logger.catch
async def static_buttons(message: Message, state: FSMContext):
    await message.answer(
        'Работа со динамическими кнопками',
        reply_markup=working_with_buttons_kb
    )
    await message.delete()
    await state.set_state(FSM_DynamicButtons.working_with_buttons)


@router.message(
    F.text == 'Список динамических кнопок',
    FSM_DynamicButtons.working_with_buttons,
    AdminRoleFilter()
)
@logger.catch
async def list_static_buttons(message: Message, state: FSMContext):
    await message.answer(
        'Список динамических кнопок',
        reply_markup=(await welcome_keyboard())
    )
    await message.delete()
    await state.set_state(FSM_DynamicButtons.working_with_buttons)


@router.message(
    F.text == 'Получить список всех кнопок',
    FSM_DynamicButtons.working_with_buttons,
    AdminRoleFilter()
)
@logger.catch
async def get_static_buttons(message: Message, state: FSMContext):
    await message.answer(
        'Список динамических кнопок',
        reply_markup=(await get_buttons_kb(dynamic=True))
    )
    await message.delete()
    await state.set_state(FSM_DynamicButtons.working_with_buttons)


@router.message(
    F.text == 'Удалить лишние кнопки',
    FSM_DynamicButtons.working_with_buttons,
    AdminRoleFilter()
)
@logger.catch
async def prepare_static_buttons(message: Message, state: FSMContext):
    r = await message.answer(
        'ВНИМАНИЕ!\n'
        'Любое нажатие на кнопку - удалит её\n\n'
        'Этот режим автоматически выключится через 15 секунд',
    )
    await asyncio.sleep(5)
    await r.delete()
    await state.set_state(FSM_DynamicButtons.delete_buttons)
    r = await message.answer(
        'Удалить лишние кнопки',
        reply_markup=(await get_buttons_for_delete(dynamic=True))
    )
    await asyncio.sleep(15)
    await r.delete()
    await state.set_state(FSM_DynamicButtons.working_with_buttons)
    await message.delete()


@router.callback_query(
    FSM_DynamicButtons.delete_buttons,
    AdminRoleFilter()
)
@logger.catch
async def delete_static_buttons(qq: CallbackQuery, state: FSMContext):
    await DbButton.delete_button(int(qq.data))
    await qq.message.edit_reply_markup(
        reply_markup=(await get_buttons_for_delete(dynamic=True))
    )


@router.message(
    F.text == 'Добавить новую кнопку',
    FSM_DynamicButtons.working_with_buttons,
    AdminRoleFilter()
)
@logger.catch
async def add_new_static_button(message: Message, state: FSMContext):
    await state.set_state(FSM_DynamicButtons.get_button_name)
    await message.answer(
        'Отправь мне текст кнопки(Не больше 20 символов)'
    )


@router.message(FSM_DynamicButtons.get_button_name,  AdminRoleFilter())
@logger.catch
async def get_button_name(message: Message, state: FSMContext):
    await state.set_data({'button_name': message.text})
    await state.set_state(FSM_DynamicButtons.get_button_link)
    await message.answer(
        'Отлично, отправь мне ссылку для кнопки(не более 44 символов)'
    )


@router.message(FSM_DynamicButtons.get_button_link,  AdminRoleFilter())
@logger.catch
async def get_button_link(message: Message, state: FSMContext):
    button_url = message.text.lower()
    if len(button_url) > 44:
        await message.answer('Слишком длинная ссылка')
        return
    if button_url.startswith('t.me'):
        button_url = f'https://{button_url}'
    if not (button_url.startswith(('https://', 'http://'))):
        await message.answer('Неверная ссылка, она должна начинаться с http:// или https://')
        return

    await DbButton.add_button(
        name=(await state.get_data()).get('button_name'),
        url=button_url,
        type=BTE.dynamic
    )
    await message.answer(
        'Кнопка добавлена',
        reply_markup=(await get_buttons_kb(dynamic=True))
    )

    await state.set_state(FSM_DynamicButtons.working_with_buttons)
