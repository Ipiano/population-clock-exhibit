from pathlib import Path
import sys

from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import QQmlApplicationEngine


class PopulationDisplay:
    def __init__(self):
        self._app = QGuiApplication(sys.argv)

        self._engine = QQmlApplicationEngine()
        self._engine.quit.connect(self._app.quit)
        self._engine.load(str(Path(__file__).parent / "main.qml"))

    def run(self):
        return self._app.exec_()
