import asyncio

from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from src.handlers import new_member, start, admin_panel
from src.settings import bot, logger


# Запуск бота
async def main():
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_routers(
            start.router,
            admin_panel.main_admin_panel_router,
            admin_panel.static_buttons_router,
            admin_panel.dynamic_buttons_router,
            new_member.router
    )
    # await bot.delete_webhook(drop_pending_updates=True)]
    r = await bot.get_me()
    logger.info(f'Бот запущен: https://t.me/{r.username}')
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
