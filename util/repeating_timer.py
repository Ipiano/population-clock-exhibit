from threading import Timer
from typing import Callable
from datetime import timedelta


class RepeatingTimer:
    """
    Like threading.Timer, but repeats until cancelled

    Only supports void -> void functions
    """

    def __init__(
        self,
        interval: timedelta,
        function: Callable[[], None],
    ):
        self._tm = None
        self._interval = interval.total_seconds()
        self._fn = function

    def start(self):
        self._tm = Timer(self._interval, self._run_and_restart)
        self._tm.start()

    def _run_and_restart(self):
        self._fn()
        self.start()

    def stop(self):
        if self._tm:
            self._tm.cancel()
        self._tm = None
