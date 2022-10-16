import logging
import requests

from population.population_data import PopulationData

LOGGER = logging.getLogger("get_census")

"""
URL of the US census population API. Returns a JSON payload with at least
{
    "population": 7915854387,
    "population_rate": 2.3441182775241,
    "rate_interval": "second",
}
"""
REQUEST_URL = "https://www.census.gov/popclock/data/population.php/world"


def get_world_census() -> PopulationData:
    response = None
    json_data = None
    try:
        response = requests.get(REQUEST_URL)
    except requests.RequestException as ex:
        LOGGER.warning("Failed to get latest population data: %s", str(ex))
        raise

    try:
        json_data = response.json()["world"]
    except requests.JSONDecodeError as ex:
        LOGGER.error("Failed to decode response: %s", response.content)
        raise

    try:
        return PopulationData(json_data)
    except Exception as ex:
        LOGGER.error(
            "Failed to read stats from json object (%s): %s",
            json_data,
            ex,
        )
