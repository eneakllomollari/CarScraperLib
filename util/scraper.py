import json
import logging

import requests
from bs4 import BeautifulSoup

from classes import Vehicle, Dealer
from consts import VIN, LISTING_ID, MAKE, MODEL, TRIM, BODY_STYLE, YEAR, PRICE, MILEAGE, VEHICLE_HREF_FORMAT, \
    NOT_APPLICABLE, NAME, PHONE_NUMBER, STREET_ADDRESS, CITY, STATE, DEALER_ADDRESS_FORMAT, RATING, REVIEW_COUNT, \
    DEALER_RATING_FORMAT, SELLER, TARGET_STATE, PAGE, VEHICLE, TOTAL_NUM_PAGES, SEARCH_URL, LISTINGS_PER_PAGE, \
    SEARCH_RADIUS, ZIP_CODE, SEARCH

logger = logging.getLogger(__name__)


def scrape_and_get_cars_list():
    query_url = SEARCH_URL.format('{}', LISTINGS_PER_PAGE, SEARCH_RADIUS, ZIP_CODE)
    url_list = get_result_url_list(query_url)
    list_vehicles = []
    for url in url_list:
        list_vehicles.append(get_list_vehicles(url))
    return list_vehicles


def get_result_url_list(url):
    first_page_url = url.format(1)
    num_pages = get_total_num_pages(first_page_url)
    url_list = []
    url_list.extend(url.format(i + 1) for i in range(num_pages))
    return url_list


def get_total_num_pages(url):
    return get_response(url)[PAGE][SEARCH][TOTAL_NUM_PAGES]


def get_list_vehicles(url):
    print(url)
    listings_dict = get_response(url)[PAGE][VEHICLE]
    cars_list = []
    for vehicle in listings_dict:
        if vehicle[SELLER][STATE] == TARGET_STATE and vehicle[VIN] is not None and vehicle[LISTING_ID] is not None:
            cars_list.append(get_vehicle(vehicle))
    return cars_list


def get_response(url):
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    listings = soup.find('head').find_all('script')
    for val in listings:
        val = val.text.strip()
        try:
            return json.loads(val[val.index('CARS.digitalData = ') + len('CARS.digitalData = '):][:-1])
        except ValueError:
            pass
    raise ValueError('CARS.digitalData was not found in `get_response()`')


def get_vehicle(vehicle_info):
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
        href=VEHICLE_HREF_FORMAT.format(vehicle_info[LISTING_ID]),
        dealer=Dealer(
            name=seller_info[NAME],
            phone_number=seller_info[PHONE_NUMBER],
            rating=DEALER_RATING_FORMAT.format(seller_info[RATING], seller_info[REVIEW_COUNT]),
            address=DEALER_ADDRESS_FORMAT.format(seller_info[STREET_ADDRESS], seller_info[CITY], seller_info[STATE])
        )
    )
