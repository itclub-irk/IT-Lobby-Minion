import asyncio

from aiogram import Dispatcher

from src.config import bot
from src.config import logger
from src.handlers import admin_panel
from src.handlers.join2group import router as join2group_router
from src.handlers.start import router as start_router


async def main():
    dp = Dispatcher()
    dp.include_routers(
        join2group_router,
        start_router,
        admin_panel.admin_panel_router,
        admin_panel.welcome_message_router,
        admin_panel.static_buttons_router,
        admin_panel.dynamic_buttons_router
    )

    r = await bot.get_me()
    logger.info(f"Бот запущен: https://t.me/{r.username}")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
