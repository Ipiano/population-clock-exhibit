from typing import Callable

from world_pop.get_census import get_latest_census
from world_pop.population_data import PopulationData
from world_pop.population_data_observer import PopulationDataObservable


class PopulationDataUpdater(PopulationDataObservable):
    """
    Observable hook for updating population stats; call update()
    from a timer or something to propagate data through the app
    """

    def __init__(
        self,
        update_fn: Callable[[], PopulationData] = get_latest_census,
    ):
        self._update_fn = update_fn

    def update(self):
        try:
            self.report_stats(self._update_fn())
        except Exception:
            pass
