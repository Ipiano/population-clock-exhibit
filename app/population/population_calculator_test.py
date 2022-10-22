import pytest
from datetime import datetime, timezone, timedelta

from population.population_calculator import PopulationCalculator
from population.population_data import PopulationData


def test_population_calculator_no_data():
    tracker = PopulationCalculator()

    assert not tracker.get_population()


def test_population_calculator_starting_data():
    base_time = datetime.now(timezone.utc).replace(microsecond=0)

    data = PopulationData()
    data.population = 0
    data.population_rate = 1
    data.population_rate_interval_ms = 1000
    data.timestamp = base_time

    tracker = PopulationCalculator(data)
    assert 0 == tracker.get_population(base_time)
    assert 1 == tracker.get_population(base_time + timedelta(seconds=1))
    assert 5 == tracker.get_population(base_time + timedelta(seconds=5))


def test_population_calculator_updated_data():
    base_time = datetime.now(timezone.utc).replace(microsecond=0)

    data = PopulationData()
    data.population = 0
    data.population_rate = 1
    data.population_rate_interval_ms = 1000
    data.timestamp = base_time

    tracker = PopulationCalculator(data)

    data.population = 4
    data.population_rate = 2
    data.population_rate_interval_ms = 100

    tracker.on_change(data)

    assert 4 == tracker.get_population(base_time)
    assert 24 == tracker.get_population(base_time + timedelta(seconds=1))


def test_population_calculator_deep_copy_data():
    base_time = datetime.now(timezone.utc).replace(microsecond=0)

    data = PopulationData()
    data.population = 0
    data.population_rate = 1
    data.population_rate_interval_ms = 1000
    data.timestamp = base_time

    tracker = PopulationCalculator(data)

    data.population = 4
    data.population_rate = 2
    data.population_rate_interval_ms = 100

    assert 1 == tracker.get_population(base_time + timedelta(seconds=1))

    tracker.on_change(data)

    data.population_rate_interval_ms = 10

    assert 24 == tracker.get_population(base_time + timedelta(seconds=1))
