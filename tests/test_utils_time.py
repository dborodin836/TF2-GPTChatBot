import pytest
import datetime

from modules.utils.time import get_date, get_minutes_from_str
from tests.common import raise_


class MockDate(datetime.date):
    @classmethod
    def today(cls):
        return cls(2024, 1, 1)


def test_epoch_time():
    assert get_date(1654005046, 1685541046) == "1 years 0 months 0 days"
    assert get_date(1527774646, 1685541046) == "5 years 0 months 0 days"
    assert get_date(1682949743, 1685541046) == "0 years 1 months 0 days"
    assert get_date(1497448943, 1685541046) == "5 years 11 months 21 days"
    assert get_date(1331474543, 1685541046) == "11 years 2 months 21 days"
    assert get_date(1685541046, 1685541046) == "0 years 0 months 0 days"


def test_epoch_time_now(mocker):
    mocker.patch.object(datetime, "date", MockDate)

    assert get_date(1654005046) == "1 years 7 months 4 days"


def test_get_minutes_from_str():
    # Minutes
    assert get_minutes_from_str("12:20") == 12
    assert get_minutes_from_str("12:60") == 12

    # Hours
    assert get_minutes_from_str("1:00:00") == 60
    assert get_minutes_from_str("1:25:00") == 85

    # Fails
    assert get_minutes_from_str("TEST") == 0
    assert get_minutes_from_str("2:") == 0
    assert get_minutes_from_str("12:62") == 0
