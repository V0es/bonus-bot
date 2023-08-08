from states import Register
from keyboards import confirm_otp_keyboard

from aiogram.dispatcher import FSMContext
from aiogram import types


import re


# TODO: register state with FSM
async def register(callback: types.CallbackQuery):
    await callback.message.answer('Вы вошли в регистрацию, введи свой номер телефона, в указанном виде, например, +79991234567')
    await Register.enter_phone_number.set()
    await callback.answer()


async def enter_fullname(message: types.Message, state: FSMContext):  # TODO: проверка на корректность фио
    answer = message.text
    await state.update_data(fullname=answer)
    data = await state.get_data()
    await message.answer(f'Отлично, регистрация завершена. Твои данные: {data}')
    await state.finish()


async def enter_phone_number(message: types.Message, state: FSMContext):  # TODO: проверка на корректность телефона
    answer = message.text
    regexp = '^\+\d{1,3}\d{3}\d{7}$'
    if not len(re.findall(regexp, answer)):
        await message.answer('Вы ввели неправильный номер телефона, попробуйте ещё раз.')
        return
    await state.update_data(phone_number=answer)
    await message.answer('Введите одноразовый пароль из SMS.', reply_markup=confirm_otp_keyboard)
    await Register.confirm_otp.set()
    

async def enter_email(message: types.Message, state: FSMContext):  # TODO: проверка на корректность почты
    answer = message.text
    await state.update_data(enter_email=answer)
    await message.answer('Отлично, теперь введи ФИО, например, Иванов Иван Иванович')
    await Register.enter_fullname.set()
    

async def resend_otp(callback: types.CallbackQuery, state: FSMContext):
    # TODO: do some stuff to resend otp and check failed attempts
    
    pass


async def confirm_otp(message: types.Message, state: FSMContext):
    answer = message.text
    if answer == '0000':
        await message.answer('Отлично, теперь введи почту.')
        await Register.enter_email.set()
    else:
        await message.answer('Вы ввели неверный пароль. Попробуйте отправить новый позже')
        
        
