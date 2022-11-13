from argparse import ArgumentParser
from pathlib import Path
from datetime import timedelta
from logging.handlers import RotatingFileHandler
import logging
import signal
import time
import sys

from population.population_data import PopulationData
from population.population_calculator import PopulationCalculator
from population.population_data_file import PopulationDataFile
from population.population_data_updater import PopulationDataUpdater
from population.population_data_observer import PopulationDataObserver
from util.repeating_timer import RepeatingTimer
from display.population_display import PopulationDisplay

LOGGER = logging.getLogger("population")
LOG_FILE = "/var/log/popclock/popclock.log"

def parse_args():
    ap = ArgumentParser(
        "Population Clock (command line)",
        description="Show the world population, according to census.gov",
    )
    ap.add_argument(
        "-i",
        "--interval",
        type=float,
        default=1,
        help="Number of seconds between calculation updates",
    )
    ap.add_argument(
        "-u",
        "--update",
        type=float,
        default="60",
        help="Number of seconds between pinging census.gov for new data",
    )
    ap.add_argument(
        "-p",
        "--path",
        type=Path,
        default="./cache",
        help="Path to directory to store cache data in",
    )
    ap.add_argument(
        "-ll",
        "--loglevel",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Log level",
    )
    ap.add_argument(
        "-g",
        "--graphical",
        action="store_true",
        help="Run a UI that displays the population",
    )
    ap.add_argument(
        "-f",
        "--fullscreen",
        action="store_true",
        help="Run a UI that displays the population (fullscreen)",
    )
    ap.add_argument(
        "--height-hack",
        type=int,
        default=0,
        help="Render in the top of the window this many pixels tall (0 for no hack)",
    )
    ap.add_help = True
    return ap.parse_args()


def main(args):
    logger = logging.getLogger()
    logger.setLevel(args.loglevel)

    formatter = logging.Formatter('%(asctime)s\t\t%(name)25s:%(levelname)-8s\t-- %(message)s')

    log_stdout = logging.StreamHandler(sys.stdout)
    log_stdout.setFormatter(formatter)

    logger.addHandler(log_stdout)

    try:
        file_handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=104857600, backupCount=5)
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
    except:
        LOGGER.warning(f"Unable to open log file {LOG_FILE}")


    data_file = PopulationDataFile(args.path)
    updater = PopulationDataUpdater()

    LOGGER.info("Loading cached population stats...")
    provider = PopulationCalculator(data_file.load())

    latest_stats = None
    class LocalObserver(PopulationDataObserver):
        def __init__(self):
            pass

        def on_change(self, data: PopulationData):
            nonlocal latest_stats
            latest_stats = data

    local_observer = LocalObserver()

    updater.add_observer(provider)
    updater.add_observer(data_file)
    updater.add_observer(local_observer)

    # Ping the site every so often
    update_timer = RepeatingTimer(timedelta(seconds=args.update), updater.update)
    update_timer.start()

    # Regardless of what the regular ping time is, ping every few seconds until the
    # first reading is available
    def initial_updates():
        nonlocal latest_stats

        if latest_stats is None:
            LOGGER.info("Attempting to get initial value...")
            updater.update()

        # Would be nice to stop the initial updates timer here
        # but I can't figure out how to properly capture it inside
        # this function to call stop() on it

    initial_timer = RepeatingTimer(timedelta(seconds=5), initial_updates)
    initial_timer.start()

    initial_updates()

    if args.graphical or args.fullscreen:
        LOGGER.info("Starting UI...")

        ui = PopulationDisplay(provider, timedelta(seconds=args.interval), fullscreen=args.fullscreen, height_hack=max(0, args.height_hack))
        ui.run()
    else:
        # Print to screen regularly
        def printout():
            pop = provider.get_population()
            if pop:
                print("World Population: {}".format(pop))
            else:
                print("Waiting to get initial statistics...")

        print_timer = RepeatingTimer(timedelta(seconds=args.interval), printout)
        print_timer.start()

        do_exit = False

        def handler(signum, frame):
            nonlocal do_exit
            do_exit = True

        signal.signal(signal.SIGINT, handler)
        signal.signal(signal.SIGABRT, handler)

        while not do_exit:
            time.sleep(0.5)

        print_timer.stop()

    update_timer.stop()
    initial_timer.stop()


if __name__ == "__main__":
    main(parse_args())
