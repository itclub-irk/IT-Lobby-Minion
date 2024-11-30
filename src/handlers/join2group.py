from venv import logger

from aiogram import F, Router
from aiogram.types import Message
from src.utils.welcome_message import configure_welcome_message
from src.utils.keyboards.join2group import welcome_keyboard

router = Router()


@router.message(F.new_chat_members)
async def welcome_new_member(message: Message):
    logger.debug(f'Пользователь {message.from_user.full_name} вступил в группу')
    for new_member in message.new_chat_members:
        await message.answer(
            text=(await configure_welcome_message(
                user_full_name=new_member.full_name,
                username=new_member.username,
                user_id=new_member.id)
            ),
            reply_markup=(await welcome_keyboard())
        )

    await message.delete()
