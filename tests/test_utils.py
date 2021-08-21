import pytest

import datetime
from tests.fixtures import times


@pytest.mark.parametrize(['from_time', 'expected'],
                         [[times.one_second_ago, datetime.timedelta(days=0, hours=0, )],
                          [times.two_second_ago, datetime.timedelta(days=0, hours=0, )],
                          [times.three_second_ago, datetime.timedelta(days=0, hours=0, )],
                          [times.one_minute_ago, datetime.timedelta(days=0, hours=0, )],
                          [times.two_minute_ago, datetime.timedelta(days=0, hours=0, )],
                          [times.three_minute_ago, datetime.timedelta(days=0, hours=0, )],
                          [times.one_hour_ago, datetime.timedelta(days=0, hours=0, )],
                          [times.one_hour_15_minute_ago, datetime.timedelta(days=0, hours=0, )],
                          [times.one_hour_30_minute_ago, datetime.timedelta(days=0, hours=0, )],
                          [times.one_hour_30_minute_5_second_ago, datetime.timedelta(days=0, hours=0, )],
                          [times.two_hour_ago, datetime.timedelta(days=0, hours=0, )],
                          [times.two_hour_30_minute_ago, datetime.timedelta(days=0, hours=0, )],
                          [times.three_hour_ago, datetime.timedelta(days=0, hours=0, )],
                          [times.one_day_ago, datetime.timedelta(days=0, hours=0, )],
                          [times.two_day_ago, datetime.timedelta(days=0, hours=0, )],
                          [times.one_month_ago, datetime.timedelta(days=0, hours=0, )],
                          [times.two_month_ago, datetime.timedelta(days=0, hours=0, )],

                          ])
def test_get_timedelta_floored_from_now(from_time, expected):
    """Testing time delta which should have some flooring capabilities"""
    pass
