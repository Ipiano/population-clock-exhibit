from typing import Dict, Any, Optional
from world_pop.population_rate import milliseconds_per


class PopulationData:
    """
    Holds stats of the population
    """

    def __init__(self, data: Optional[Dict[str, Any]] = None):
        if data:
            self._population = int(data["population"])
            self._population_rate = float(data["population_rate"])

            # When we get the data from the server, they give rate interval as a
            # unit (second, year, etc.); but when we save/reload it, it's been
            # converted to the equivalent number of milliseconds
            if "rate_interval" in data:
                self._rate_interval_ms = milliseconds_per(data["rate_interval"])
            else:
                assert "rate_interval_ms" in data
                self._rate_interval_ms = int(data["rate_interval_ms"])
        else:
            self._population = 0
            self._population_rate = 0
            self._rate_interval_ms = 1

        assert self._population >= 0
        assert self._rate_interval_ms > 0

    @property
    def population(self) -> int:
        return self._population

    @population.setter
    def population(self, value: int):
        assert value >= 0
        self._population = value

    @property
    def population_rate(self) -> float:
        return self._population_rate

    @population_rate.setter
    def population_rate(self, value: float):
        self._population_rate = value

    @property
    def population_rate_interval_ms(self) -> int:
        return self._rate_interval_ms

    @population_rate_interval_ms.setter
    def population_rate_interval_ms(self, value: int):
        assert value > 0
        self._rate_interval_ms = value
