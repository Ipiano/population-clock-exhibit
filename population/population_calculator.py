from typing import Optional
from datetime import datetime, timezone
from copy import deepcopy

from population.population_data import PopulationData
from population.population_data_observer import PopulationDataObserver
from population.population_provider import PopulationProvider


def population_now(data: PopulationData, when: Optional[datetime] = None) -> int:
    when = when or datetime.now(timezone.utc)
    delta_ms = (when - data.timestamp).total_seconds() * 1000

    return data.population + data.population_rate * (
        delta_ms / data.population_rate_interval_ms
    )


class PopulationCalculator(PopulationDataObserver, PopulationProvider):
    def __init__(self, initial_data: Optional[PopulationData] = None):
        self._data = deepcopy(initial_data)

    def on_change(self, stats: PopulationData):
        self._data = deepcopy(stats)

    def get_population(self, when: Optional[datetime] = None) -> Optional[int]:
        if self._data:
            return population_now(self._data, when)
        return None
