from abc import *

from population.population_data import PopulationData


class PopulationDataObserver(ABC):
    @abstractmethod
    def on_change(self, stats: PopulationData):
        pass


class PopulationDataObservable:
    def __init__(self):
        self._observers = set()

    def add_observer(self, observer: PopulationDataObserver):
        self._observers.add(observer)

    def remove_observer(self, observer: PopulationDataObserver):
        self._observers.remove(observer)

    def report_stats(self, data: PopulationData):
        for o in self._observers:
            o.on_change(data)
