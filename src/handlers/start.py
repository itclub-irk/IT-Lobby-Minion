from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.keyboards import keyboards
from src.settings import BOT_ADMIN_ID

router = Router()


@router.message(Command('start'))
@router.message(F.text == 'Вернуться в меню')
async def start(message: Message, state: FSMContext):
    if message.chat.type == 'private' and message.from_user.id == BOT_ADMIN_ID:
        await message.answer(
                text='Привет!\nТут ты можешь настроить приветственное сообщение',
                reply_markup=keyboards.admin_panel_kb
        )
    else:
        await message.answer(
                text='Бот доступен только владельцу @lobbyirk'
        )
    await state.clear()
