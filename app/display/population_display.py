from pathlib import Path
from datetime import timedelta
import sys
import signal

from util.repeating_timer import RepeatingTimer
from population.population_provider import PopulationProvider

from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import QQmlApplicationEngine
from PySide2.QtCore import QTimer, QObject, Signal, Property


class PopulationDisplay:
    class PopulationBridge(QObject):
        def __init__(self):
            QObject.__init__(self)
            self._population = None

        def set_population(self, pop: int):
            self._population = str(pop) if pop else None
            self.population_changed.emit()

        def get_population(self):
            return self._population

        @Signal
        def population_changed(self):
            pass

        population = Property(str, get_population, notify=population_changed)

    def __init__(
        self,
        population_provider: PopulationProvider,
        update_interval: timedelta = timedelta(seconds=1),
    ):
        self._app = QGuiApplication(sys.argv)

        self._engine = QQmlApplicationEngine()
        self._engine.quit.connect(self._app.quit)

        self._bridge = PopulationDisplay.PopulationBridge()
        self._engine.rootContext().setContextProperty(
            "population_provider", self._bridge
        )

        self._data_provider = population_provider

        def update():
            self._bridge.set_population(self._data_provider.get_population())

        self._timer = RepeatingTimer(update_interval, update)
        self._engine.load(str(Path(__file__).parent / "main.qml"))

    def run(self):
        # Define a no-op timer that returns control back to the python
        # interpreter every so often so that a sigint can get handled
        # correctly to shut down the app
        def noop():
            pass

        timer = QTimer()
        timer.setInterval(500)
        timer.setSingleShot(False)
        timer.timeout.connect(noop)
        timer.start()

        def handler(signum, frame):
            QGuiApplication.quit()

        signal.signal(signal.SIGINT, handler)
        signal.signal(signal.SIGABRT, handler)

        self._timer.start()
        ret = self._app.exec_()
        self._timer.stop()

        return ret
