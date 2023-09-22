from telegram_bot.states import Register
from telegram_bot.keyboards import (confirm_otp_keyboard as confirm_otp_kb,
                                    get_registered_start_keyboard as reg_start_kb,
                                    get_back_to_main_menu_keyboard as back_to_mainmenu_kb)

from telegram_bot.db.requests import add_user, change_email, change_phone_number

from aiogram.fsm.context import FSMContext
from aiogram import types, Router

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from telegram_bot.exceptions import UserAlreadyExists, UserNotFoundException

from telegram_bot.utils.otp import generate_otp
from telegram_bot.utils.web import sms_auth
from telegram_bot.utils.validators import validate_email, validate_fullname, validate_otp_codes, validate_phone_number


router = Router()


@router.callback_query()
async def register(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        'Вы вошли в регистрацию, введи свой номер телефона, в указанном виде, например, +79991234567'
    )
    await state.set_state(Register.enter_phone_number)
    await callback.answer()


@router.message()
async def enter_phone_number(message: types.Message, state: FSMContext):
    """
    Handler for getting user phone number
    """
    answer = message.text
    if not validate_phone_number(answer):
        await message.answer('Неверный формат номера телефона, попробуйте ещё раз.')
        return
    await state.update_data(phone_number=answer)
    otp_code = generate_otp()
    await state.update_data(otp_code=otp_code)
    sms_auth.sendSMS(recipients=answer[1:], message=f'{otp_code}')
    await message.answer(
        'В ближайшее время вам на телефон поступит звонок от робота, который продиктует 4-значный одноразовый пароль.\n'
        'Для подтверждения введите полученный пароль',
        reply_markup=confirm_otp_kb
    )
    await state.set_state(Register.confirm_otp)


@router.message()
async def enter_email(message: types.Message, state: FSMContext):
    answer = message.text
    if not validate_email(answer):
        await message.answer('Похоже, вы ввели некорректный адрес электронной почты. '
                             'Проверьте правильность введённого ранее адреса или попробуйте другой.')
        return
    await state.update_data(email=answer)
    await message.answer('Введите, пожалуйста, ваши имя и фамилию для профиля. Например, Иван Иванов')
    await state.set_state(Register.enter_fullname)


@router.callback_query()
async def resend_otp(callback: types.CallbackQuery, state: FSMContext):
    # TODO: check failed attempts

    data = await state.get_data()
    phone_number = data.get('phone_number')
    otp_code = generate_otp()
    await state.update_data(otp_code=otp_code)
    sms_auth.sendSMS(recipients=phone_number[1:], message=f'{otp_code}')
    await callback.message.edit_text(
        'В ближайшее время вам на телефон поступит звонок от робота, который продиктует 4-значный одноразовый пароль.\n'
        'Для подтверждения введите полученный пароль')
    await state.set_state(Register.confirm_otp)


@router.message()
async def confirm_otp(message: types.Message, state: FSMContext, session: AsyncSession):
    answer = message.text
    data = await state.get_data()
    valid_code = data.get('otp_code')
    if answer == valid_code:  # check if user entered valid otp

        if data.get('prev_state') == 'change_email':
            try:
                await change_email(session, message.from_user.id, data.get('new_email'))
            except UserNotFoundException:
                await message.answer('Произошёл сбой, повторите попытку позже')
                await state.clear()
                return
            except IntegrityError:
                await message.answer(
                    'Произошла ошибка, вероятно, уже сущестувет пользователь с таким адресом электронной почты',
                    reply_markup=back_to_mainmenu_kb())
                await state.clear()
                return
            await message.answer(f'Вы успешно сменили почту. Ваш новый email: {data.get("new_email")}',
                                 reply_markup=back_to_mainmenu_kb())
            await state.clear()
            return

        elif data.get('prev_state') == 'change_phone_number':

            try:  # catch several exceptions
                await change_phone_number(session, message.from_user.id, data.get('new_phone_number'))
            except UserNotFoundException:
                await message.answer('Произошёл сбой, повторите попытку позже')
                await state.clear()
                return
            except IntegrityError:
                await message.answer(
                    'Произошла ошибка, вероятно, уже сущестувет пользователь с таким номером телефона',
                    reply_markup=back_to_mainmenu_kb()
                )
                await state.clear()
                return

            await message.answer(
                f'Вы успешно сменили номер телефона. Ваш новый номер: {data.get("new_phone_number")}',
                reply_markup=back_to_mainmenu_kb()
            )
            await state.clear()
            return

        await message.answer('Отлично, теперь введи почту.')
        await state.set_state(Register.enter_email)

    else:  # if user entered invalid otp
        await state.update_data(otp_code=None)  # this otp is no longer available
        await state.set_state(Register.resend_otp)
        await message.answer('Вы ввели неверный пароль. Попробуйте отправить новый', reply_markup=confirm_otp_kb)


@router.message()
async def enter_fullname(message: types.Message, state: FSMContext,
                         session: AsyncSession):  # TODO: проверка на корректность фио
    answer = message.text
    if not validate_fullname(answer):
        await message.answer(
            'Недоступные символы в имени, попробуйте ещё раз.',
            reply_markup=back_to_mainmenu_kb()
        )
        return
    await state.update_data(fullname=answer)
    data = await state.get_data()

    try:
        await add_user(session=session, state_data=data, user_id=message.from_user.id)
    except UserAlreadyExists:
        await message.answer('Такой пользователь уже существует!')
        await state.clear()
        return
    await state.clear()
    await message.answer('Отлично, регистрация завершена.', reply_markup=reg_start_kb())
