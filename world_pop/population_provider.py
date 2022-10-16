import abc
from typing import Optional
from datetime import datetime


class PopulationProvider(abc.ABC):
    @abc.abstractmethod
    def get_population(self, when: Optional[datetime] = None) -> Optional[int]:
        pass
