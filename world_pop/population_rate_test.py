from world_pop.population_rate import milliseconds_per, UnknownUnitError

import pytest


def test_milliseconds_per_millisecond():
    assert milliseconds_per("millisecond") == 1


def test_milliseconds_per_second():
    assert milliseconds_per("second") == 1000


def test_milliseconds_per_minute():
    assert milliseconds_per("minute") == 60000


def test_milliseconds_per_hour():
    assert milliseconds_per("hour") == 3600000


def test_milliseconds_per_invalid():
    with pytest.raises(UnknownUnitError):
        milliseconds_per("not a time")
