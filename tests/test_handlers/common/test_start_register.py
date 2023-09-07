import pytest

from unittest.mock import AsyncMock, Mock

from aiogram.fsm.storage.memory import MemoryStorage

from telegram_bot.keyboards import (get_unregistered_start_keyboard as unreg_start_kb,
                                    get_registered_start_keyboard as reg_start_kb,
                                    get_back_to_main_menu_keyboard as back_to_mainmenu_kb)

from telegram_bot.handlers.common.start import start_unregistered, start_registered
from telegram_bot.handlers.common.register import (register, resend_otp, confirm_otp,
                                                   enter_fullname, enter_phone_number, enter_email)
from telegram_bot.states import Register
from tests.mocked_bot import MockedBot
from tests.utils import create_state


@pytest.mark.asyncio
async def test_start_ungregistered():
    message = AsyncMock()
    await start_unregistered(message)

    message.answer.assert_called_with(
        'Здравствуйте, кажется, вы не зарегистрированы в нашей системе.',
        reply_markup=unreg_start_kb())


@pytest.mark.asyncio
async def test_start_registered():
    message = AsyncMock()
    await start_registered(message)

    message.answer.assert_called_with(
        'Привет, я бот бонусной программы. Нажми кнопнку ниже, чтобы войти в главное меню.',
        reply_markup=reg_start_kb())


@pytest.mark.asyncio
async def test_register(storage, bot):
    call = AsyncMock()
    state = create_state(storage, bot)
    await register(call, state)

    call.message.edit_text.assert_called_with(
        'Вы вошли в регистрацию, введи свой номер телефона, в указанном виде, например, +79991234567'
    )
    assert await state.get_state() == Register.enter_phone_number

    call.answer.assert_any_call()


@pytest.mark.asyncio
async def test_enter_phone_number(storage, bot):
    message = AsyncMock()
    message.text = '+70000000000'
    state = create_state(storage, bot)
    await enter_phone_number(message, state)

    assert await state.get_state() == Register.confirm_otp


@pytest.mark.asyncio
async def test_resend_otp(storage, bot):
    call = AsyncMock()
    state = create_state(storage, bot)
    await state.update_data(phone_number='123')
    await resend_otp(call, state)

    call.message.edit_text.assert_called_with(
        'В ближайшее время вам на телефон поступит звонок от робота, который продиктует 4-значный одноразовый пароль.\n'
        'Для подтверждения введите полученный пароль'
    )

    assert await state.get_state() == Register.confirm_otp


@pytest.mark.asyncio
async def test_confirm_otp_email(storage: MemoryStorage, bot: MockedBot, mocker: Mock):
    mocker.patch(
        'telegram_bot.handlers.common.register.change_email'
    )
    message = AsyncMock()
    message.text = '0000'
    state = create_state(storage, bot)
    await state.update_data(otp_code='0000')
    await state.update_data(new_email='test')

    # change_email
    await state.update_data(prev_state='change_email')
    await confirm_otp(message, state, AsyncMock())
    message.answer.assert_called_with(
        f'Вы успешно сменили почту. Ваш новый email: test',
        reply_markup=back_to_mainmenu_kb()
    )
    assert await state.get_state() is None


@pytest.mark.asyncio
async def test_confirm_otp_phone(storage: MemoryStorage, bot: MockedBot, mocker: Mock):
    mocker.patch(
        'telegram_bot.handlers.common.register.change_phone_number'
    )
    message = AsyncMock()
    message.text = '0000'
    state = create_state(storage, bot)
    await state.update_data(otp_code='0000')
    await state.update_data(new_phone_number='test')

    # change_phone_number
    await state.update_data(prev_state='change_phone_number')
    await confirm_otp(message, state, AsyncMock())
    message.answer.assert_called_with(
        f'Вы успешно сменили номер телефона. Ваш новый номер: test',
        reply_markup=back_to_mainmenu_kb()
    )
    assert await state.get_state() is None


@pytest.mark.asyncio
async def test_confirm_otp_default(storage: MemoryStorage, bot: MockedBot):
    message = AsyncMock()
    message.text = '0000'
    state = create_state(storage, bot)
    # default
    await state.update_data(otp_code='0000')
    await confirm_otp(message, state, AsyncMock())
    message.answer.assert_called_with(
        'Отлично, теперь введи почту.'
    )
    assert await state.get_state() == Register.enter_email


@pytest.mark.asyncio
async def test_enter_fullname(storage: MemoryStorage, bot: MockedBot, mocker: Mock):
    mocker.patch(
        'telegram_bot.handlers.common.register.change_email'
    )
    message = AsyncMock()
    state = create_state(storage, bot)

    # Test valid fullname
    message.text = 'Test Test'
    await enter_fullname(message, state, AsyncMock())
    message.answer.assert_called_with(
        'Отлично, регистрация завершена.',
        reply_markup=reg_start_kb()
    )
    assert await state.get_state() is None

    # Test invalid fullname
    await state.set_state(Register.enter_fullname)  # set state to initial value for this handler
    message.text = 'Test Test@'
    await enter_fullname(message, state, AsyncMock())
    message.answer.assert_called_with(
        'Недоступные символы в имени, попробуйте ещё раз.',
        reply_markup=back_to_mainmenu_kb()
    )
    assert await state.get_state() == Register.enter_fullname  # check if state was not changed


@pytest.mark.asyncio
async def test_enter_email(storage, bot):
    message = AsyncMock()
    state = create_state(storage, bot)

    # Test valid email
    message.text = 'test@test.test'
    await enter_email(message, state)
    message.answer.assert_called_with('Введите, пожалуйста, ваши имя и фамилию для профиля. Например, Иван Иванов')
    assert await state.get_state() == Register.enter_fullname

    # Test invalid email
    await state.set_state(Register.enter_email)  # set state to initial value for this handler
    message.text = 'test@@sd.'
    await enter_email(message, state)
    message.answer.assert_called_with(
        'Похоже, вы ввели некорректный адрес электронной почты. '
        'Проверьте правильность введённого ранее адреса или попробуйте другой.'
    )
    assert await state.get_state() == Register.enter_email  # check if state was not changed
