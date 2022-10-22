from typing import Callable
import logging

from population.get_census import get_world_census
from population.population_data import PopulationData
from population.population_data_observer import PopulationDataObservable

LOGGER = logging.getLogger("population.updater")


class PopulationDataUpdater(PopulationDataObservable):
    """
    Observable hook for updating population stats; call update()
    from a timer or something to propagate data through the app
    """

    def __init__(
        self,
        update_fn: Callable[[], PopulationData] = get_world_census,
    ):
        PopulationDataObservable.__init__(self)
        self._update_fn = update_fn

    def update(self):
        try:
            LOGGER.info("Updating population statistics...")
            self.report_stats(self._update_fn())
        except Exception:
            pass
