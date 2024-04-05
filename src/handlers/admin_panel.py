import asyncio

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from src import keyboards
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


@router.message(F.text == 'Получить список всех кнопок')
async def get_all_buttons(message: Message, state: FSMContext):
    await message.answer(
            'Список кнопок',
            reply_markup=keyboards.welcome_message_kb(1_000)
    )
    await state.clear()


@router.message(F.text == 'Отредактировать кнопки')
async def edit_buttons(message: Message, state: FSMContext):
    await state.set_state(FSM_admin_panel.edit_buttons)
    r = await message.answer(
            'Работа с кнопками',
            reply_markup=keyboards.edit_buttons_kb
    )


@router.message(FSM_admin_panel.edit_buttons and F.text == 'Удалить лишние кнопки')
async def delete_buttons(message: Message, state: FSMContext):
    r = await message.answer(
            text='<b>!!!Режим удаления кнопок!!!</b>\n\n'
                 'Через 30 секунд он автоматически выключится\n\n'
                 'Нажми на кнопку и она исчезнет',
    )
    await asyncio.sleep(5)
    await r.delete()
    r = await message.answer(
            text='<b>!!!Режим удаления кнопок!!!</b>\n\n'
                 'Через 30 секунд он автоматически выключится\n\n'
                 'Нажми на кнопку и она исчезнет',
            reply_markup=keyboards.welcome_message_kb_without_urls(),
    )
    await state.set_state(FSM_admin_panel.delete_buttons)
    await asyncio.sleep(30)
    await state.clear()
    await r.delete()


@router.callback_query(FSM_admin_panel.delete_buttons)
async def delete_inline_button(qq: CallbackQuery):
    repository.remove_button(qq.data)
    await qq.message.edit_text(
            text=qq.message.html_text,
            reply_markup=keyboards.welcome_message_kb_without_urls(),
    )


@router.message(FSM_admin_panel.edit_buttons and F.text == 'Добавить новую кнопку')
async def add_button(message: Message, state: FSMContext):
    await message.answer('Отправь мне текст кнопки\n\nМожешь использовать смайлики')
    await state.set_state(FSM_admin_panel.get_button_name)


@router.message(FSM_admin_panel.get_button_name)
async def get_button_name(message: Message, state: FSMContext):
    await message.answer('Отлично, отправь мне ссылку')
    await state.set_data({'button_name': message.text})
    await state.set_state(FSM_admin_panel.get_button_link)


@router.message(FSM_admin_panel.get_button_link)
async def get_button_link(message: Message, state: FSMContext):
    button_name = (await state.get_data())['button_name']
    button_link = message.text
    repository.add_button(name=button_name, url=button_link)
    await message.answer('Кнопка добавлена')
    await state.clear()


@router.message(FSM_admin_panel.get_message)
async def get_message(message: Message, state: FSMContext):
    repository.set_welcome_message_text(message.html_text)
    await message.answer('Текст для приветственного сообщения установлен')
    await state.clear()
