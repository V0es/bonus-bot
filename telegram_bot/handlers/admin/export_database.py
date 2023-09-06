from datetime import datetime

from aiogram import types, Router
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.fsm.context import FSMContext

from telegram_bot.utils.export import DBExport
from telegram_bot.keyboards import get_back_to_main_menu_keyboard as back_to_mainmenu_kb
from telegram_bot.states import AdminState

router = Router()


@router.callback_query()
async def export_database(callback: types.CallbackQuery, state: FSMContext, session: AsyncSession):
    await state.set_state(AdminState.export)
    db_export = DBExport(session)
    print(db_export)
    export_file = await db_export.upload_to_excel()
    print('datetime: ', datetime.now())
    await callback.message.answer_document(
        document=export_file,
        caption=f'Выгрузка базы данных пользователей на {datetime.now().strftime("%d-%m-%Y_%H-%M-%S")}',
        reply_markup=back_to_mainmenu_kb()
        )
    await callback.answer()
