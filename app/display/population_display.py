from pathlib import Path
from datetime import timedelta
import sys
import signal

from util.repeating_timer import RepeatingTimer
from population.population_provider import PopulationProvider

from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import QQmlApplicationEngine
from PySide2.QtCore import QTimer, QObject, Signal, Property, QLocale


class PopulationDisplay:
    class PopulationBridge(QObject):
        def __init__(self, height_hack=0):
            QObject.__init__(self)
            self._population = None
            self._fullscreen = False
            self._source = None
            self._height_hack = height_hack

        def set_population(self, pop: int):
            loc = QLocale(QLocale.English, QLocale.UnitedStates)
            self._population = loc.toString(pop) if pop else None
            self.population_changed.emit()

        def get_population(self):
            return self._population

        @Signal
        def population_changed(self):
            pass

        def set_fullscreen(self, fs: bool):
            self._fullscreen = fs
            self.fullscreen_changed.emit()

        def get_fullscreen(self):
            return self._fullscreen

        @Signal
        def fullscreen_changed(self):
            pass

        def get_height_hack(self):
            return self._height_hack

        @Signal
        def height_hack_changed(self):
            pass

        def set_source(self, source: str):
            if source != self._source:
                self._source = source
                self.source_changed.emit()

        def get_source(self):
            return self._source or ""

        @Signal
        def source_changed(self):
            pass

        population = Property(str, get_population, notify=population_changed)
        fullscreen = Property(
            bool, get_fullscreen, set_fullscreen, notify=fullscreen_changed
        )
        height_hack = Property(int, get_height_hack, notify=height_hack_changed)
        source = Property(str, get_source, notify=source_changed)

    def __init__(
        self,
        population_provider: PopulationProvider,
        update_interval: timedelta = timedelta(seconds=1),
        fullscreen: bool = False,
        height_hack: int = 0,
    ):
        self._app = QGuiApplication(sys.argv)

        self._engine = QQmlApplicationEngine()
        self._engine.quit.connect(self._app.quit)

        self._bridge = PopulationDisplay.PopulationBridge(height_hack)
        self._bridge.set_fullscreen(fullscreen)

        self._engine.rootContext().setContextProperty(
            "population_provider", self._bridge
        )

        self._data_provider = population_provider

        def update():
            self._bridge.set_population(self._data_provider.get_population())
            self._bridge.set_source(self._data_provider.get_population_source())

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
