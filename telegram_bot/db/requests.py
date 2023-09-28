import logging

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from asyncpg.exceptions import UniqueViolationError

from typing import Dict, Sequence

from telegram_bot.db.models import User

from telegram_bot.config import config

from telegram_bot.exceptions import UserNotFoundException, UserAlreadyExists


async def add_user(session: AsyncSession, state_data: Dict, user_id: int) -> None:
    phone_number = state_data.get('phone_number')
    fullname = state_data.get('fullname')
    email = state_data.get('email')
    if user_id == int(config.owner_id) or user_id == int(config.dev_id):
        owner_flag = True
    else:
        owner_flag = False
    # noinspection PyArgumentList
    user = User(user_id=user_id,
                phone_number=phone_number,
                fullname=fullname,
                email=email,
                is_admin=owner_flag,
                is_owner=owner_flag)  # is_admin could be changed later by owner;
    # if user is owner by default => he is admin a priori
    try:
        session.add(user)
    except UniqueViolationError:
        raise UserAlreadyExists

    await session.commit()
    logging.info(f'User : {user} added')


async def get_all_users(session: AsyncSession) -> Sequence[User]:
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
    await session.execute(
        update(User).where(User == user).values({User.bonus_points: User.bonus_points + bonus_points_to_add})
    )
    await session.commit()
    logging.info(f'{bonus_points_to_add} bonus points added to user: {user}')


async def delete_all(session: AsyncSession) -> None:
    await session.execute(delete(User).where(User.id >= 1))
    await session.commit()
    logging.critical('DELETED ALL USERS')


async def delete_user(session: AsyncSession, user: User) -> None:
    await session.execute(delete(User).where(User == user))
    await session.commit()
    logging.warning(f'DELETED USER: {user}')


async def set_admin(session: AsyncSession, phone_number: str) -> None:
    user = await get_user_by_phone_number(session, phone_number)
    await session.execute(update(User).where(User == user).values({User.is_admin: True}))
    await session.commit()
    logging.info(f'Administrator rights are enabled for user: {user}')


async def remove_admin(session: AsyncSession, phone_number: str) -> None:
    user = await get_user_by_phone_number(session, phone_number)
    await session.execute(update(User).where(User == user).values({User.is_admin: False}))
    await session.commit()
    logging.info(f'Administrator rights are disabled for user: {user}')


async def is_admin(session: AsyncSession, user_id: int) -> bool:
    user = await get_user_by_id(session, user_id)
    return user.is_admin


async def is_owner(session: AsyncSession, user_id: int) -> bool:
    user = await get_user_by_id(session, user_id)
    return user.is_owner


async def change_email(session: AsyncSession, user_id: int, new_email: str) -> None:
    user = await get_user_by_id(session, user_id)
    await session.execute(update(User).where(User == user).values({User.email: new_email}))
    await session.commit()
    logging.info(f'User: {user} has changed email')


async def change_fullname(session: AsyncSession, user_id: int, new_fullname: str) -> None:
    user = await get_user_by_id(session, user_id)
    await session.execute(update(User).where(User == user).values({User.fullname: new_fullname}))
    await session.commit()
    logging.info(f'User: {user} has changed fullname')


async def change_phone_number(session: AsyncSession, user_id: int, new_phone_number: str) -> None:
    user = await get_user_by_id(session, user_id)
    await session.execute(update(User).where(User == user).values({User.phone_number: new_phone_number}))
    await session.commit()
    logging.info(f'User: {user} has changed phone_number')


async def change_bonus_points(session: AsyncSession, recipient_phone_number: str, new_account: int) -> None:
    user = await get_user_by_phone_number(session, recipient_phone_number)
    await session.execute(update(User).where(User == user).values({User.bonus_points: new_account}))
    await session.commit()
    logging.info(f'Account for user: {user} has been set to {new_account}')
