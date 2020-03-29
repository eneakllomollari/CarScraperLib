import json

import requests
from bs4 import BeautifulSoup

from pscraper.utils.misc import measure_time
from .consts import CARS_COM_QUERY, PAGE, SEARCH, TOTAL_NUM_PAGES
from ..consts import LISTING_ID, PHONE_NUMBER, SELLER, STATE, VEHICLE, VIN
from ..helpers import update_vehicle


@measure_time
def scrape_cars(zip_code, search_radius, target_states, api):
    """ Scrape EV data from cars.com filtering with the specified parameters

    Args:
        zip_code (str): The zip code to perform the search in
        search_radius (str): The search radius for the specified zip code
        target_states (list): The states to search in (i.e. ```['CA', 'NV']```)
        api (pscraper.api.API): Pscraper API to communicate with the backend

    Returns:
        total (int): Total number of cars scraped
    """
    url = CARS_COM_QUERY.format('{}', search_radius, zip_code)
    total = 0
    num_pages = _get_cars_com_response(url.format(1))[PAGE][SEARCH][TOTAL_NUM_PAGES]
    for i in range(num_pages):
        vehicles = _get_cars_com_response(url.format(i))[PAGE][VEHICLE]
        for vehicle in vehicles:
            is_eligible_vehicle = all((vehicle[VIN], vehicle[LISTING_ID], vehicle[SELLER][PHONE_NUMBER]))
            if vehicle[SELLER][STATE] in target_states and is_eligible_vehicle:
                update_vehicle(vehicle, api)
                total += 1
    return total


def _get_cars_com_response(url):
    token = 'CARS.digitalData = '
    for val in BeautifulSoup(requests.get(url).text, 'html.parser').find('head').find_all('script'):
        val = val.text.strip()
        try:
            return json.loads(val[val.index(token) + len(token):][:-1])
        except ValueError:
            pass
    raise ValueError(f'cars.com response data was not found!\n\t{url}')
