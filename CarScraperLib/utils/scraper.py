import json

import requests
from bs4 import BeautifulSoup

from ..classes import Vehicle, Dealer
from ..consts import VIN, LISTING_ID, MAKE, MODEL, TRIM, BODY_STYLE, YEAR, PRICE, MILEAGE, NOT_APPLICABLE, NAME, \
    CARS_COM_VEHICLE_HREF_FORMAT, PHONE_NUMBER, STREET_ADDRESS, CITY, STATE, DEALER_ADDRESS_FORMAT, RATING, VEHICLE, \
    REVIEW_COUNT, DEALER_RATING_FORMAT, SELLER, PAGE, TOTAL_NUM_PAGES, CARS_COM_SEARCH_URL, SEARCH, LISTINGS_PER_PAGE


def scrape_and_get_vehicle_list(zip_code, search_radius, target_state):
    """ TODO Add functionality for more websites, only support `cars.com` so far
    :param zip_code: the zip code to search in
    :param search_radius: the search radius for the zip code
    :param target_state: the US state to search in (i.e. 'CA')
    :return: a list of `classes.Car` objects
    """
    query_url = CARS_COM_SEARCH_URL.format('{}', LISTINGS_PER_PAGE, search_radius, zip_code)
    return _scrape_and_get_cars_com_vehicles(query_url, target_state)


def _scrape_and_get_cars_com_vehicles(url, target_state):
    num_pages = _get_cars_com_response(url.format(1))[PAGE][SEARCH][TOTAL_NUM_PAGES]
    list_vehicles = []
    for i in range(num_pages):
        list_vehicles.extend(_get_list_cars_com_vehicles(url.format(i), target_state))
    return list_vehicles


def _get_list_cars_com_vehicles(url, target_state):
    cars_list = []
    for vehicle in _get_cars_com_response(url)[PAGE][VEHICLE]:
        if vehicle[SELLER][STATE] == target_state and all((vehicle[VIN], vehicle[LISTING_ID])):
            cars_list.append(_get_vehicle_object(vehicle))
    return cars_list


def _get_cars_com_response(url):
    for val in BeautifulSoup(requests.get(url).text, 'html.parser').find('head').find_all('script'):
        val = val.text.strip()
        try:
            return json.loads(val[val.index('CARS.digitalData = ') + len('CARS.digitalData = '):][:-1])
        except ValueError:
            pass
    raise ValueError('CARS.digitalData was not found in `_get_cars_com_response()`, url: {}'.format(url))


def _get_vehicle_object(vehicle_info):
    seller_info = vehicle_info[SELLER]
    return Vehicle(
        listing_id=vehicle_info[LISTING_ID],
        vin=vehicle_info[VIN],
        make=vehicle_info[MAKE],
        model=vehicle_info[MODEL],
        trim=vehicle_info[TRIM],
        body_style=vehicle_info[BODY_STYLE],
        price=vehicle_info[PRICE],
        mileage=vehicle_info[MILEAGE],
        year=vehicle_info[YEAR],
        first_date=NOT_APPLICABLE,
        last_date=NOT_APPLICABLE,
        duration=NOT_APPLICABLE,
        href=CARS_COM_VEHICLE_HREF_FORMAT.format(vehicle_info[LISTING_ID]),
        dealer=Dealer(
            name=seller_info[NAME],
            phone_number=seller_info[PHONE_NUMBER],
            rating=DEALER_RATING_FORMAT.format(seller_info[RATING], seller_info[REVIEW_COUNT]),
            address=DEALER_ADDRESS_FORMAT.format(seller_info[STREET_ADDRESS], seller_info[CITY], seller_info[STATE])
        )
    )
