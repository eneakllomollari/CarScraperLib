from hamcrest import assert_that, is_in

from .consts import ALLOWED_RD, STATES
from .marketplaces.autotrader import scrape_autotrader
from .marketplaces.carmax import scrape_carmax
from .marketplaces.cars import scrape_cars


def scrape(zip_code, search_radius, target_states, api):
    """ Scrape data about electric vehicles from all supported marketplaces using the specified parameters

    Args:
        zip_code (str): The zip code to perform the search in
        search_radius (int): The search radius for the specified zip code
        target_states (list): The states to search in (i.e. ```['CA', 'NV']```)
        api (pscraper.api.PscraperAPI): Pscraper API to communicate with the DB

    Returns:
        list of tuples: (elapsed time and total vehicles) per marketplace

    """
    assert_that(search_radius, is_in(ALLOWED_RD))
    assert_that(set(target_states).issubset(set(STATES)))

    cars_et, cars_total = scrape_cars(zip_code, search_radius, target_states, api)
    autotrader_et, autotrader_total = scrape_autotrader(zip_code, search_radius, target_states, api)
    carmax_et, carmax_total = scrape_carmax(zip_code, search_radius, target_states, api)

    return (cars_et, cars_total), (autotrader_et, autotrader_total), (carmax_et, carmax_total)
