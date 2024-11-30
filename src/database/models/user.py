from datetime import UTC, datetime

from sqlalchemy import BigInteger, select
from sqlalchemy.orm import Mapped, mapped_column

from src.schemas import UserSchema
from src.database.connection import Base, async_session_maker


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    full_name: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        nullable=False, default=datetime.now
    )

    @classmethod
    async def add_user(cls, user_id, full_name):
        if await cls.get_user(user_id):
            return
        async with async_session_maker() as session:
            session.add(cls(id=user_id, full_name=full_name))
            await session.commit()

    @classmethod
    async def get_user(cls, user_id: int) -> UserSchema:
        async with async_session_maker() as session:
            user = await session.get(cls, user_id)
            return UserSchema(
                id=user.id,
                full_name=user.full_name,
                created_at=user.created_at
            ) if user else None

    @classmethod
    async def get_all_users(cls) -> list[UserSchema]:
        async with async_session_maker() as session:
            users = await session.execute(
                select(cls)
            )
            return [
                UserSchema(
                    id=user.id,
                    full_name=user.full_name,
                    created_at=user.created_at
                ) for user in (users.scalars())
            ] if users else []
