import pytest
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Tuple
from datetime import datetime, timezone

from population.population_data import PopulationData
from population.population_data_file import PopulationDataFile


@pytest.fixture
def test_file() -> Tuple[Path, str]:
    temp_dir = TemporaryDirectory()
    yield (Path(temp_dir.name), "test.json")


def test_load_missing_file(test_file):
    data_file = PopulationDataFile(test_file[0], test_file[1])
    assert not data_file.load()


def test_load_empty_file(test_file):
    file_path = test_file[0] / test_file[1]
    file_path.touch()
    assert file_path.exists()

    data_file = PopulationDataFile(test_file[0], test_file[1])
    assert not data_file.load()


def test_load_non_json_file(test_file):
    with open(test_file[0] / test_file[1], "w") as f:
        f.write("Hello World!")

    data_file = PopulationDataFile(test_file[0], test_file[1])
    assert not data_file.load()


def test_load_json_file_with_wrong_structure(test_file):
    data = {"hello": "world"}
    json.dump(data, open(test_file[0] / test_file[1], "w"))

    data_file = PopulationDataFile(test_file[0], test_file[1])
    assert not data_file.load()


def test_load_wrong_type_population(test_file):
    data = {
        "population": "world",
        "population_rate": "0.123",
        "rate_interval": "second",
    }
    json.dump(data, open(test_file[0] / test_file[1], "w"))

    data_file = PopulationDataFile(test_file[0], test_file[1])
    assert not data_file.load()


def test_load_wrong_type_population_rate(test_file):
    data = {
        "population": "500",
        "population_rate": "xyz",
        "rate_interval": "second",
    }
    json.dump(data, open(test_file[0] / test_file[1], "w"))

    data_file = PopulationDataFile(test_file[0], test_file[1])
    assert not data_file.load()


def test_load_wrong_type_rate_interval(test_file):
    data = {
        "population": "500",
        "population_rate": "0.123",
        "rate_interval": "not a time",
    }
    json.dump(data, open(test_file[0] / test_file[1], "w"))

    data_file = PopulationDataFile(test_file[0], test_file[1])
    assert not data_file.load()


def test_load_valid_file(test_file):
    data = {
        "population": "500",
        "population_rate": "0.123",
        "rate_interval": "millisecond",
        "updated": "0",
    }
    json.dump(data, open(test_file[0] / test_file[1], "w"))

    data_file = PopulationDataFile(test_file[0], test_file[1])
    pop_data = data_file.load()

    assert pop_data is not None
    assert pop_data.population == 500
    assert pop_data.population_rate == 0.123
    assert pop_data.population_rate_interval_ms == 1


def test_save_file(test_file):
    data = PopulationData()

    data.population = 10
    data.population_rate = 0.123
    data.population_rate_interval_ms = 100

    # We don't save beyond second precision
    data.timestamp = datetime.now(timezone.utc).replace(microsecond=0)

    data_file = PopulationDataFile(test_file[0], test_file[1])
    data_file.save(data)

    new_data = PopulationData(json.load(open(test_file[0] / test_file[1])))
    assert new_data.population == data.population
    assert new_data.population_rate == data.population_rate
    assert new_data.population_rate_interval_ms == data.population_rate_interval_ms
    assert new_data.timestamp == data.timestamp
