import xlsxwriter
import os
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.types import FSInputFile
import datetime

from db.requests import get_all_users


class DBExport:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.filename = self._generate_name()
        self.filepath = rf'telegram_bot\utils\export\export_{self.filename}.xlsx'

    def __del__(self):
        res = self._delete_file(self.filepath)
        if res is None:
            print('File not found')

    @staticmethod
    def _generate_name() -> str:
        return f'{datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S")}'

    @staticmethod
    def _delete_file(filepath: str):
        try:
            os.remove(filepath)
            return filepath
        except FileNotFoundError:
            return None

    async def upload_to_excel(self) -> FSInputFile:
        workbook = xlsxwriter.Workbook(self.filepath)
        worksheet = workbook.add_worksheet()

        date_format = workbook.add_format({'num_format': 'd mmmm yyyy HH:MM:SS'})  # add date format
        
        user_list = await get_all_users(self.session)
        clients = list(filter(lambda user: not (user.is_admin or user.is_owner), user_list))
        export_cols = ['id', 'timestamp', 'telegram_id', 'fullname', 'phone_number', 'email', 'bonus_points']
        for index, col in enumerate(export_cols):
            worksheet.write(0, index, col)
        for index, client in enumerate(clients):
            worksheet.write(index + 1, 0, index + 1)
            worksheet.write_datetime(index + 1, 1, client.timestamp, date_format)
            worksheet.write(index + 1, 2, client.user_id)
            worksheet.write(index + 1, 3, client.fullname)
            worksheet.write(index + 1, 4, client.phone_number)
            worksheet.write(index + 1, 5, client.email)
            worksheet.write(index + 1, 6, client.bonus_points)
        
        workbook.close()
        export_table = FSInputFile(self.filepath, self.filename)
        return export_table
