from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from typing import List

from telegram_bot.db.models import User


async def add_user(session: AsyncSession, user: User) -> None:
    await session.add(user)
    await session.commit()


async def get_all_users(session: AsyncSession) -> List[User]:
    result = await session.execute(select(User))
    return result.scalars().all()


async def get_user_by_phone_number(session: AsyncSession, phone_number: str) -> User:
    result = await session.execute(select(User).where(User.phone_number == phone_number))
    return result.scalar_one_or_none()


async def get_user_by_id(session: AsyncSession, user_id: int) -> User:
    result = await session.execute(select(User).where(User.user_id == user_id))
    return result.scalar_one_or_none()


async def add_bonus_points(session: AsyncSession, bonus_points_to_add: int, user: User) -> int:
    result = await session.execute(update(User).where(User == user).values({User.bonus_points: User.bonus_points + bonus_points_to_add}))
    await session.commit()
    return result


async def delete_all(session: AsyncSession) -> None:
    await session.execute(delete(User).where(User.id >= 1))
    await session.commit()


async def delete_user(session: AsyncSession, user: User) -> None:
    await session.execute(delete(User).where(User == user))
    await session.commit()
