from aiogram import types, Router
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.fsm.context import FSMContext

from utils.export import DBExport
from keyboards import get_back_to_main_menu_keyboard as back_to_mainmenu_kb
from states import AdminState

router = Router()


@router.callback_query()
async def export_database(callback: types.CallbackQuery, state: FSMContext, session: AsyncSession):
    await state.set_state(AdminState.export)
    db_export = DBExport(session)
    export_file = await db_export.upload_to_excel()
    await callback.message.answer_document(
        document=export_file,
        caption=f'Выгрузка базы данных пользователей на {db_export.filename}',
        reply_markup=back_to_mainmenu_kb()
        )
    await callback.answer()
