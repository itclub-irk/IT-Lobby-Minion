import asyncio

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from src import keyboards, settings
from src.database import repository
from src.states import FSM_StaticButtons

router = Router()


@router.message(F.text == 'статические кнопки')
async def static_buttons(message: Message, state: FSMContext):
    await state.set_state(FSM_StaticButtons.working_with_buttons)
    await message.answer(text='Редактирование статических кнопок', reply_markup=keyboards.working_with_buttons_kb)


@router.message(F.text == 'Получить список всех кнопок', FSM_StaticButtons.working_with_buttons)
async def get_all_buttons(message: Message):
    await message.answer(
            'Список статических кнопок',
            reply_markup=keyboards.static_or_dynamic_buttons_kb(settings.STATIC_BUTTONS_CONFIG_NAME)
    )


@router.message(FSM_StaticButtons.working_with_buttons, F.text == 'Удалить лишние кнопки')
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
            reply_markup=keyboards.welcome_message_kb_without_urls(settings.STATIC_BUTTONS_CONFIG_NAME),
    )
    await state.set_state(FSM_StaticButtons.delete_buttons)
    await asyncio.sleep(30)
    await state.clear()
    await r.delete()


@router.callback_query(FSM_StaticButtons.delete_buttons)
async def delete_inline_button(qq: CallbackQuery):
    repository.remove_button(qq.data, button_config_name=settings.STATIC_BUTTONS_CONFIG_NAME)
    await qq.message.edit_text(
            text=qq.message.html_text,
            reply_markup=keyboards.welcome_message_kb_without_urls(
                    buttons_config_name=settings.STATIC_BUTTONS_CONFIG_NAME)
    )


@router.message(
        F.text == 'Добавить новую кнопку', FSM_StaticButtons.working_with_buttons
)
async def add_button(message: Message, state: FSMContext):
    await message.answer('Отправь мне текст кнопки\n\nМожешь использовать смайлики')
    await state.set_state(FSM_StaticButtons.get_button_name)


@router.message(FSM_StaticButtons.get_button_name)
async def get_button_name(message: Message, state: FSMContext):
    await message.answer('Отлично, отправь мне ссылку')
    await state.set_data({'button_name': message.text})
    await state.set_state(FSM_StaticButtons.get_button_link)


@router.message(FSM_StaticButtons.get_button_link)
async def get_button_link(message: Message, state: FSMContext):
    button_name = (await state.get_data())['button_name']
    button_link = message.text
    repository.add_button(name=button_name, url=button_link, button_config_name=settings.STATIC_BUTTONS_CONFIG_NAME)
    await message.answer('Кнопка добавлена')
    await state.set_state(FSM_StaticButtons.working_with_buttons)
