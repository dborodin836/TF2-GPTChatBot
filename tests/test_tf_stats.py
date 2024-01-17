from modules.utils.time import get_date


def test_epoch_time():
    assert get_date(1654005046, 1685541046) == "1 years 0 months 0 days"
    assert get_date(1527774646, 1685541046) == "5 years 0 months 0 days"
    assert get_date(1682949743, 1685541046) == "0 years 1 months 0 days"
    assert get_date(1497448943, 1685541046) == "5 years 11 months 21 days"
    assert get_date(1331474543, 1685541046) == "11 years 2 months 21 days"
    assert get_date(1685541046, 1685541046) == "0 years 0 months 0 days"
