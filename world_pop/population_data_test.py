import pytest

from world_pop.population_data import PopulationData


def test_missing_population():
    data = {
        "population_rate": "0.123",
        "rate_interval": "millisecond",
    }

    with pytest.raises(Exception):
        pop = PopulationData(data)


def test_invalid_population_type():
    data = {
        "population_rate": "0.123",
        "rate_interval": "millisecond",
        "population": "abc",
    }

    with pytest.raises(Exception):
        pop = PopulationData(data)


def test_invalid_population_value():
    data = {
        "population_rate": "0.123",
        "rate_interval": "millisecond",
        "population": "-1",
    }

    with pytest.raises(Exception):
        pop = PopulationData(data)


def test_missing_population_rate():
    data = {
        "population": "1",
        "rate_interval": "millisecond",
    }

    with pytest.raises(Exception):
        pop = PopulationData(data)


def test_invalid_population_rate_type():
    data = {
        "population": "1",
        "population_rate": "abc",
        "rate_interval": "millisecond",
    }

    with pytest.raises(Exception):
        pop = PopulationData(data)


def test_missing_rate_interval():
    data = {
        "population": "1",
        "population_rate": "0.123",
    }

    with pytest.raises(Exception):
        pop = PopulationData(data)


def test_invalid_rate_interval_value():
    data = {
        "population": "1",
        "population_rate": "0.123",
        "rate_interval": "not a time unit",
    }

    with pytest.raises(Exception):
        pop = PopulationData(data)


def test_load_rate_interval():
    data = {"population": "1", "population_rate": "0.123", "rate_interval": "second"}

    pop = PopulationData(data)
    assert pop.population == 1
    assert pop.population_rate == 0.123
    assert pop.population_rate_interval_ms == 1000


def test_invalid_rate_interval_ms_type():
    data = {"population": "1", "population_rate": "0.123", "rate_interval_ms": "abc"}

    with pytest.raises(Exception):
        pop = PopulationData(data)


def test_invalid_rate_interval_ms_value():
    data = {"population": "1", "population_rate": "0.123", "rate_interval_ms": "-50"}

    with pytest.raises(Exception):
        pop = PopulationData(data)


def test_load_rate_interval_ms():
    data = {"population": "1", "population_rate": "0.123", "rate_interval_ms": "1000"}

    pop = PopulationData(data)
    assert pop.population == 1
    assert pop.population_rate == 0.123
    assert pop.population_rate_interval_ms == 1000
