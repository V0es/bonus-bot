import unittest.mock as mock
import datetime


class MockDatetime:
    def __init__(self, target: str, now: datetime):
        self.now = now
        self.target = target

    def __enter__(self):
        self.patcher = mock.patch(self.target)
        mock_dt = self.patcher.start()
        mock_dt.now.return_value = self.now.replace(tzinfo=None)
        mock_dt.datetime.side_effect = lambda *args, **kw: datetime.datetime(*args, **kw)
        return mock_dt

    def __exit__(self, *args, **kwargs):
        self.patcher.stop()
