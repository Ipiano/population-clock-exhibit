from pathlib import Path
from typing import Optional
import requests
import json
import logging

LOGGER = logging.Logger("data_provider")

"""
URL of the US census population API. Returns a JSON payload with at least
{
    "population": 7915854387,
    "population_rate": 2.3441182775241,
    "rate_interval": "second",
}
"""
REQUEST_URL = "https://www.census.gov/popclock/data/population.php/world"


def get_latest_census() -> Optional[dict]:
    try:
        response = requests.get(REQUEST_URL)
    except requests.RequestException as ex:
        LOGGER.log(logging.WARN, "Failed to get latest population data: %s", str(ex))
        return None

    try:
        return response.json()
    except requests.JSONDecodeError as ex:
        LOGGER.log(logging.ERROR, "Failed to decode response: %s", response.content)
        return None


"""
Default location to cache the most recent result from the above URL so that if
the internet isn't available, we can still provide a reasonable guess
"""
CACHE_DIR = Path("/var/cache/pop_clock")
CACHE_FILE = "world_pop.json"


class PopulationStats:
    """
    Holds stats of the population
    """

    def __init__(self, data):
        self._population = data["population"]
        self._population_rate = data["population_rate"]
        self._rate_interval = data["rate_interval"]

    @property
    def population(self) -> int:
        return self._population

    @property
    def population_rate(self) -> float:
        return self._population_rate

    @property
    def population_rate_interval(self) -> str:
        return self._rate_interval


class PopulationClockDataProvider:
    """
    Get population data for the world

    This class will regularly attempt to ping the us census site
    to get updated data. Data will be cached locally, so that if
    the internet is not available, something reasonably close can
    be returned
    """

    def __init__(self, cache_dir: Path = CACHE_DIR, updater=get_latest_census):
        """
        cache_dir: Directory to store cache files in. Must be writable
        """
        self._cache_file = cache_dir / CACHE_FILE
        self._stats = self._load_from_file(self._cache_file)

    def get_stats(self) -> Optional[PopulationStats]:
        """
        Get the latest stats data, if it's known
        """
        return self._stats

    def _load_from_file(self, file: Path) -> Optional[PopulationStats]:
        """
        Read a cache file. Returns None if the file does not exist or contains
        the wrong data
        """
        pass

    def _save_to_file(self, file: Path, data: dict):
        with open(file) as f:
            json.dump(data, f)

    def _update_stats(self, new_data: dict):
        """
        If the new data is valid, update the internal values and save it in the
        cache file
        """
        pass
