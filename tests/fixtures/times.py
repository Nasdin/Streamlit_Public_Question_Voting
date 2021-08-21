""" These fixtures assumes that the time is on 11am 28 June """
import datetime
from functools import partial
import pytest

_year_month_day = partial(datetime.datetime,
                          year=2021,
                          month=6,
                          day=28)

_year_month = partial(datetime.datetime,
                      year=2021, month=6)


@pytest.fixture()
def one_month_ago():
    return datetime.datetime(year=2021,
                             month=5,
                             day=28)


@pytest.fixture()
def two_month_ago():
    return datetime.datetime(year=2021,
                             month=4,
                             day=28)


@pytest.fixture()
def one_day_ago():
    return _year_month(day=27)


@pytest.fixture()
def two_day_ago():
    return _year_month(day=26)


@pytest.fixture()
def one_hour_ago():
    return _year_month_day(hour=10)


@pytest.fixture()
def one_hour_15_minute_ago():
    return _year_month_day(hour=10,
                           minute=45)


@pytest.fixture()
def one_hour_30_minute_ago():
    return _year_month_day(hour=10,
                           minute=30)


@pytest.fixture()
def one_hour_30_minute_5_second_ago():  # Just to test that seconds makes no difference
    return _year_month_day(hour=10,
                           minute=30,
                           second=55)


@pytest.fixture()
def two_hour_ago():
    return _year_month_day(hour=9,
                           )


@pytest.fixture()
def two_hour_30_minute_ago():
    return _year_month_day(hour=9,
                           minute=30
                           )


@pytest.fixture()
def three_hour_ago():
    return _year_month_day(hour=8,
                           )


@pytest.fixture()
def one_minute_ago():
    return _year_month_day(hour=10,
                           minute=59)


@pytest.fixture()
def two_minute_ago():
    return _year_month_day(hour=10,
                           minute=58)


@pytest.fixture()
def three_minute_ago():
    return _year_month_day(hour=10,
                           minute=57)


@pytest.fixture()
def one_second_ago():
    return _year_month_day(hour=10,
                           minute=59,
                           second=59)


@pytest.fixture()
def two_second_ago():
    return _year_month_day(hour=10,
                           minute=59,
                           second=58)


@pytest.fixture()
def three_second_ago():
    return _year_month_day(hour=10,
                           minute=59,
                           second=57)
