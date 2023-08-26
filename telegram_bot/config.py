from typing import Optional

import os

from sqlalchemy.engine import URL

from dotenv import load_dotenv


class Config():
    
    def __init__(self) -> None:
        self.load_env()
        self.bot_token: str = self.get_variable('bot_token')
        print(self.bot_token)
        self.bot_fsm_storage: str = self.get_variable('bot_fsm_storage')
        self.pg_user: str = self.get_variable('POSTGRES_USERNAME')
        self.pg_pass: str | None = self.get_variable('POSTGRES_PASSWORD')
        self.pg_host: str = self.get_variable('POSTGRES_HOST')
        self.pg_port: str = self.get_variable('POSTGRES_PORT')
        self.db_name: str = self.get_variable('db_name')
        self.db_url = self._get_db_url()
        self.debug = self.validate_debug(self.get_variable('debug'))
        self.sms_project_name: str = self.get_variable('sms_project_name')
        self.sms_api_key: str = self.get_variable('sms_api_key')
        self.admin_id: str = self.get_variable('admin_id')
        self.redis_host: str = self.get_variable('redis_host')
        self.redis_port: str = self.get_variable('redis_port')
        self.redis_username: str = self.get_variable('redis_username')
        self.redis_password: str = self.get_variable('redis_password')

    @staticmethod
    def load_env():
        load_dotenv()
    
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
    
    def _get_redis_url(self) -> URL:
        return URL.create(

        )

    @staticmethod
    def validate_debug(val: str):
        return False if val == 'False' else True


config = Config()
