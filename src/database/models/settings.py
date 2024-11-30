from sqlalchemy import update
from sqlalchemy.orm import Mapped, mapped_column

from src.database.connection import Base, async_session_maker
from src.schemas import SettingsSchema


class Settings(Base):
    __tablename__ = 'settings'
    id: Mapped[int] = mapped_column(nullable=False, primary_key=True)
    dynamic_button_count: Mapped[int] = mapped_column(nullable=False)
    welcome_message: Mapped[str] = mapped_column(nullable=False)

    @classmethod
    async def get_settings(cls) -> SettingsSchema:
        async with async_session_maker() as session:
            settings = await session.get(cls, 1)

            return SettingsSchema(
                id=settings.id,
                dynamic_button_count=settings.dynamic_button_count,
                welcome_message=settings.welcome_message
            )

    @classmethod
    async def set_settings(
            cls, dynamic_button_count: int = None,
            welcome_message: str = None
    ):
        """
       Updates the dynamic button count or welcome message.

       Parameters:
       ----------
       dynamic_button_count : int, optional
           Number of dynamic buttons to display.
       welcome_message : str, optional
           Text for the welcome message.

       Notes:
       -----
       Only updates the record if at least one parameter is provided.
       """
        async with async_session_maker() as session:
            if await session.get(cls, 1):
                if not (dynamic_button_count or welcome_message):
                    return
                query = update(cls).where(cls.id == 1)
                if dynamic_button_count:
                    query = query.values(dynamic_button_count=dynamic_button_count)
                if welcome_message:
                    query = query.values(
                        welcome_message=welcome_message)
                await session.execute(
                    query
                )
                await session.commit()
