import pytest
import datetime


@pytest.fixture(autouse=True, scope='session')
def time_now():
    from _pytest.monkeypatch import MonkeyPatch
    monkeypatch = MonkeyPatch()

    class FakeDateTime(datetime.datetime):
        @classmethod
        def now(cls, tz=None):
            return datetime.datetime(year=2021,
                                     month=6,
                                     day=28,
                                     hour=11,
                                     minute=0,
                                     second=0)

    monkeypatch.setattr(datetime, "datetime", FakeDateTime)
