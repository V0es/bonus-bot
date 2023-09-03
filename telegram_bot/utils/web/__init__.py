from .auth_api import AuthAPI

from ...config import config

sms_auth = AuthAPI(config.sms_project_name, config.sms_api_key)
