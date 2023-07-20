from states import Register


from aiogram.dispatcher import FSMContext
from aiogram import types



# register state with FSM
async def register(callback: types.CallbackQuery):
    await callback.message.answer('Вы вошли в регистрацию, введи полное имя. Например, Иванов Иван Иванович')
    await Register.enter_fullname.set()
    await callback.answer()


async def enter_fullname(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(name=answer)
    fullname = await state.get_data('name')
    await message.answer(f'Ваше имя: {fullname}')
    await state.finish()