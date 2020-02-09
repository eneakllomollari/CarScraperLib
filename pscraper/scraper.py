import json

import requests
from bs4 import BeautifulSoup

from pscraper.classes.vehicle import Vehicle
from pscraper._consts import VIN, LISTING_ID, VEHICLE, SELLER, PAGE, TOTAL_NUM_PAGES, CARS_COM_SEARCH_URL, \
    SEARCH, LISTINGS_PER_PAGE, STATE


def scrape(zip_code, search_radius, target_states):
    """Scrape data about electric vehicles on `cars.com` using the specified parameters

    Args:
        zip_code (str): The zip code to perform the search in
        search_radius (str): The search radius for the specified zip code
        target_states (list): The states to search in (i.e. ```['CA', 'NV']```)

    Returns:
        list: List of scraped vehicle objects

    """
    query_url = CARS_COM_SEARCH_URL.format('{}', LISTINGS_PER_PAGE, search_radius, zip_code)
    return _get_cars_com_vehicles(query_url, target_states)


def _get_cars_com_vehicles(url, target_states):
    num_pages = _get_cars_com_json_response(url.format(1))[PAGE][SEARCH][TOTAL_NUM_PAGES]
    list_vehicles = []
    for i in range(num_pages):
        for vehicle in _get_cars_com_json_response(url.format(i))[PAGE][VEHICLE]:
            if vehicle[SELLER][STATE] in target_states and all((vehicle[VIN], vehicle[LISTING_ID])):
                list_vehicles.append(Vehicle(vehicle))
    return list_vehicles


def _get_cars_com_json_response(url):
    for val in BeautifulSoup(requests.get(url).text, 'html.parser').find('head').find_all('script'):
        val = val.text.strip()
        try:
            return json.loads(val[val.index('CARS.digitalData = ') + len('CARS.digitalData = '):][:-1])
        except ValueError:
            pass
    raise ValueError(f'CARS.digitalData was not found!\n\t{url}')
