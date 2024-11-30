from sqlalchemy import Enum, delete, select
from sqlalchemy.orm import Mapped, mapped_column

from src.schemas import ButtonTypeEnum, KbButtonSchema
from src.database.connection import Base, async_session_maker


class Button(Base):
    __tablename__ = 'buttons'
    id: Mapped[int] = mapped_column(nullable=False, primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    url: Mapped[str] = mapped_column(nullable=False)
    type: Mapped[ButtonTypeEnum] = mapped_column(Enum(ButtonTypeEnum), nullable=False)

    @classmethod
    async def get_all_buttons(cls) -> list[KbButtonSchema]:
        async with async_session_maker() as session:
            buttons = (await session.execute(select(cls))).scalars().all()

            return [
                KbButtonSchema(
                    id=button.id,
                    name=button.name,
                    url=button.url,
                    type=button.type
                ) for button in buttons
            ] if buttons else []

    @classmethod
    async def add_button(cls, name: str, url: str, type: ButtonTypeEnum):
        async with async_session_maker() as session:
            session.add(cls(name=name, url=url, type=type))
            await session.commit()

    @classmethod
    async def delete_button(cls, button_id: int):
        async with async_session_maker() as session:
            await session.execute(delete(cls).where(cls.id == button_id))
            await session.commit()
