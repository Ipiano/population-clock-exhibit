from pathlib import Path
from typing import Optional
import json
import logging

from population.population_data_observer import PopulationDataObserver
from population.population_data import PopulationData

"""
Default location to cache the most recent population data so that if
the internet isn't available, we can still provide a reasonable guess
"""
DEFAULT_CACHE_DIR = Path("/var/cache/pop_clock")
DEFAULT_CACHE_FILENAME = "world_pop.json"

LOGGER = logging.Logger("data_file")


class PopulationDataFile(PopulationDataObserver):
    """
    Loads/Stores population data in a file on disk
    """

    def __init__(
        self,
        cache_dir: Path = DEFAULT_CACHE_DIR,
        cache_filename: str = DEFAULT_CACHE_FILENAME,
    ):
        self._data = None
        self._file_path = cache_dir / cache_filename

    def load(self) -> Optional[PopulationData]:
        try:
            loaded_data = None

            with open(self._file_path) as f:
                loaded_data = json.load(f)

            return PopulationData(loaded_data)
        except Exception as e:
            LOGGER.warning(
                "Failed to load population data file: %s - %s", self._file_path, e
            )
            return None

    def save(self, stats: PopulationData):
        with open(self._file_path, "w") as f:
            json.dump(stats.to_json(), f)

    def on_change(self, stats: PopulationData):
        self.save(stats)
