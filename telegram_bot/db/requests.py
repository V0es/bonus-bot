from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from typing import List, Dict

from db.models import User

from exceptions import UserNotFoundException


async def add_user(session: AsyncSession, state_data: Dict, user_id: int) -> None:
    phone_number = state_data.get('phone_number')
    fullname = state_data.get('fullname')
    email = state_data.get('email')
    user = User(user_id=user_id, phone_number=phone_number, fullname=fullname, email=email)
    print('ADD USER FUNCTION, SESSION: ', session)
    session.add(user)
    await session.commit()


async def get_all_users(session: AsyncSession) -> List[User]:
    result = await session.execute(select(User))
    return result.scalars().all()


async def get_user_by_phone_number(session: AsyncSession, phone_number: str) -> User | None:
    result = await session.execute(select(User).where(User.phone_number == phone_number))
    user = result.scalar_one_or_none()
    if not user:
        raise UserNotFoundException
    return user


async def get_user_by_id(session: AsyncSession, user_id: int) -> User:
    result = await session.execute(select(User).where(User.user_id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise UserNotFoundException
    return user


async def add_bonus_points(session: AsyncSession, bonus_points_to_add: int, phone_number: str) -> None:
    user = await get_user_by_phone_number(session, phone_number)
    await session.execute(update(User).where(User == user).values({User.bonus_points: User.bonus_points + bonus_points_to_add}))
    await session.commit()


async def delete_all(session: AsyncSession) -> None:
    await session.execute(delete(User).where(User.id >= 1))
    await session.commit()


async def delete_user(session: AsyncSession, user: User) -> None:
    await session.execute(delete(User).where(User == user))
    await session.commit()


async def set_admin(session: AsyncSession, phone_number: str) -> None:
    user = await get_user_by_phone_number(session, phone_number)
    await session.execute(update(User).where(User == user).values({User.is_admin: True}))
    await session.commit()
