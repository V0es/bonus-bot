from requests.auth import AuthBase


class Bearer(AuthBase):
    def __init__(self, api_key: str):
        self.api_key = api_key

    def __call__(self, req):
        req.headers['Authorization'] = f'Bearer {self.api_key}'
        return req
