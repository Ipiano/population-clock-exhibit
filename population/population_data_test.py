import pytest
from datetime import datetime, timedelta, timezone

from population.population_data import PopulationData

EPOCH = datetime(1970, 1, 1, tzinfo=timezone.utc)


def test_missing_population():
    data = {
        "population_rate": "0.123",
        "rate_interval": "millisecond",
        "updated": "1234",
    }

    with pytest.raises(Exception):
        pop = PopulationData(data)


def test_invalid_population_type():
    data = {
        "population_rate": "0.123",
        "rate_interval": "millisecond",
        "population": "abc",
        "updated": "1234",
    }

    with pytest.raises(Exception):
        pop = PopulationData(data)


def test_invalid_population_value():
    data = {
        "population_rate": "0.123",
        "rate_interval": "millisecond",
        "population": "-1",
        "updated": "1234",
    }

    with pytest.raises(Exception):
        pop = PopulationData(data)


def test_missing_population_rate():
    data = {"population": "1", "rate_interval": "millisecond", "updated": "1234"}

    with pytest.raises(Exception):
        pop = PopulationData(data)


def test_invalid_population_rate_type():
    data = {
        "population": "1",
        "population_rate": "abc",
        "rate_interval": "millisecond",
        "updated": "1234",
    }

    with pytest.raises(Exception):
        pop = PopulationData(data)


def test_missing_rate_interval():
    data = {"population": "1", "population_rate": "0.123", "updated": "1234"}

    with pytest.raises(Exception):
        pop = PopulationData(data)


def test_invalid_rate_interval_value():
    data = {
        "population": "1",
        "population_rate": "0.123",
        "rate_interval": "not a time unit",
        "updated": "1234",
    }

    with pytest.raises(Exception):
        pop = PopulationData(data)


def test_missing_timestamp():
    data = {"population": "1", "population_rate": "0.123", "rate_interval": "1"}

    with pytest.raises(Exception):
        pop = PopulationData(data)


def test_invalid_timestamp_value():
    data = {
        "population": "1",
        "population_rate": "0.123",
        "rate_interval": "1000",
        "updated": "abcd",
    }

    with pytest.raises(Exception):
        pop = PopulationData(data)


def test_load_rate_interval():
    data = {
        "population": "1",
        "population_rate": "0.123",
        "rate_interval": "second",
        "updated": "1234",
    }

    pop = PopulationData(data)
    assert pop.population == 1
    assert pop.population_rate == 0.123
    assert pop.population_rate_interval_ms == 1000
    assert pop.timestamp == EPOCH + timedelta(seconds=1234)


def test_invalid_rate_interval_ms_type():
    data = {
        "population": "1",
        "population_rate": "0.123",
        "rate_interval_ms": "abc",
        "updated": "1234",
    }

    with pytest.raises(Exception):
        pop = PopulationData(data)


def test_invalid_rate_interval_ms_value():
    data = {
        "population": "1",
        "population_rate": "0.123",
        "rate_interval_ms": "-50",
        "updated": "1234",
    }

    with pytest.raises(Exception):
        pop = PopulationData(data)


def test_load_rate_interval_ms():
    data = {
        "population": "1",
        "population_rate": "0.123",
        "rate_interval_ms": "1000",
        "updated": "1234",
    }

    pop = PopulationData(data)
    assert pop.population == 1
    assert pop.population_rate == 0.123
    assert pop.population_rate_interval_ms == 1000
    assert pop.timestamp == EPOCH + timedelta(seconds=1234)
