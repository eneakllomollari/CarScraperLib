from os import environ

from pscraper.api import API
from .consts import REPORT_FORMAT
from .sellers.autotrader import scrape_autotrader
from .sellers.carmax import scrape_carmax
from .sellers.cars import scrape_cars


def scrape(zip_code, search_radius, target_states):
    """ Scrape data about electric vehicles from all supported sellers using the specified parameters
    You need credentials with admin permissions to be set to environment variables
     `PSCRAPER_USERNAME` and `PSCRAPER_PASSWORD`

    Args:
        zip_code (str): The zip code to perform the search in
        search_radius (str): The search radius for the specified zip code
        target_states (list): The states to search in (i.e. ```['CA', 'NV']```)

    Returns:
        total: Report formatted with the total number of scraped vehicles per site

    """
    api = API(username=environ['PSCRAPER_USERNAME'], password='PSCRAPER_PASSWORD')
    cars_total = scrape_cars(zip_code, search_radius, target_states, api)
    autot_total = scrape_autotrader(zip_code, search_radius, target_states, api)
    carmax_total = scrape_carmax(zip_code, search_radius, target_states, api)
    return REPORT_FORMAT.format(cars_total, autot_total, carmax_total, api)
