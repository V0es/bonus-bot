from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.exc import IntegrityError

from typing import List, Dict

from db.models import User

from config import config

from exceptions import UserNotFoundException, UserAlreadyExists


async def add_user(session: AsyncSession, state_data: Dict, user_id: int) -> None:
    phone_number = state_data.get('phone_number')
    fullname = state_data.get('fullname')
    email = state_data.get('email')
    if user_id == config.owner_id or user_id == config.dev_id:
        owner_flag = True
    else:
        owner_flag = False
    user = User(user_id=user_id, phone_number=phone_number, fullname=fullname, email=email, is_admin=owner_flag)
    try:
        session.add(user)
    except IntegrityError:
        raise UserAlreadyExists
    
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


async def remove_admin(session: AsyncSession, phone_number: str) -> None:
    user = await get_user_by_phone_number(session, phone_number)
    await session.execute(update(User).where(User == user).values({User.is_admin: False}))
    await session.commit()


async def is_admin(session: AsyncSession, user_id: int) -> bool:
    user = await get_user_by_id(session, user_id)
    return user.is_admin


async def is_owner(session: AsyncSession, user_id: int) -> bool:
    user = await get_user_by_id(session, user_id)
    return user.is_owner


async def change_email(session: AsyncSession, user_id: str, new_email: str) -> None:
    user = await get_user_by_id(session, user_id)
    await session.execute(update(User).where(User == user).values({User.email: new_email}))
    await session.commit()


async def change_fullname(session: AsyncSession, user_id: str, new_fullname: str) -> None:
    user = await get_user_by_id(session, user_id)
    await session.execute(update(User).where(User == user).values({User.fullname: new_fullname}))
    await session.commit()


async def change_phone_number(session: AsyncSession, user_id: str, new_phone_number: str) -> None:
    user = await get_user_by_id(session, user_id)
    await session.execute(update(User).where(User == user).values({User.phone_number: new_phone_number}))
    await session.commit()


async def change_bonus_points(session: AsyncSession, recipient_phone_number: str, new_account: int) -> None:
    user = await get_user_by_phone_number(session, recipient_phone_number)
    await session.execute(update(User).where(User == user).values({User.bonus_points: new_account}))
    await session.commit()
