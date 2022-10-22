from argparse import ArgumentParser
from pathlib import Path
from datetime import timedelta
import logging
import signal
import time

from population.population_calculator import PopulationCalculator
from population.population_data_file import PopulationDataFile
from population.population_data_updater import PopulationDataUpdater
from population.population_provider import PopulationProvider
from util.repeating_timer import RepeatingTimer


def parse_args():
    ap = ArgumentParser(
        "Population Clock (command line)",
        description="Show the world population, according to census.gov",
    )
    ap.add_argument(
        "-i",
        "--interval",
        type=int,
        default=1,
        help="Number of seconds between calculation updates",
    )
    ap.add_argument(
        "-u",
        "--update",
        type=int,
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
    ap.add_help = True
    return ap.parse_args()


def main(args):
    logging.basicConfig()
    logging.getLogger().setLevel(args.loglevel)

    data_file = PopulationDataFile(args.path)
    updater = PopulationDataUpdater()
    provider = PopulationCalculator(data_file.load())

    updater.add_observer(provider)
    updater.add_observer(data_file)

    # Initial update to get us started
    updater.update()

    # Ping the site every so often
    update_timer = RepeatingTimer(timedelta(seconds=args.update), updater.update)
    update_timer.start()

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

    update_timer.stop()
    print_timer.stop()


if __name__ == "__main__":
    main(parse_args())
