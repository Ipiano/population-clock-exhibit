import pytest
import time
from datetime import timedelta

from util.repeating_timer import RepeatingTimer


def test_repeating_timer():
    """
    Just validate that this thing will update multiple times in a short
    interval; don't care about accuracy
    """
    count = 0

    def update():
        nonlocal count
        count += 1

    timer = RepeatingTimer(timedelta(milliseconds=1), update)

    timer.start()
    time.sleep(0.010)
    timer.stop()

    assert count > 5
    old_count = count

    time.sleep(0.010)
    assert count == old_count
