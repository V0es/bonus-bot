from typing import Optional

import os

from sqlalchemy.engine import URL

from dotenv import load_dotenv


class Config():
    
    def __init__(self) -> None:
        self.load_env()
        self.bot_token: str = self.get_variable('bot_token')
        self.bot_fsm_storage: str = self.get_variable('bot_fsm_storage')
        self.pg_user: str = self.get_variable('pg_user')
        self.pg_pass: str | None = self.get_variable('pg_pass')
        self.pg_host: str = self.get_variable('pg_host')
        self.pg_port: str = self.get_variable('pg_port')
        self.db_name: str = self.get_variable('db_name')
        self.db_url = self._get_db_url()
        self.debug = self.validate_debug(self.get_variable('debug'))

    @staticmethod
    def load_env():
        load_dotenv('.env')
    
    @staticmethod
    def get_variable(key: str) -> str:
        return os.getenv(key)
    
    def _get_db_url(self) -> URL:
        return URL.create(
            drivername='postgresql+asyncpg',
            username=self.pg_user,
            password=self.pg_pass,
            host=self.pg_host,
            port=self.pg_port,
            database=self.db_name
        )
    
    @staticmethod
    def validate_debug(val: str):
        return False if val == 'False' else True


config = Config()
