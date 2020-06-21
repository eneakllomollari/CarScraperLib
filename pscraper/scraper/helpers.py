import json
from datetime import datetime
from logging import getLogger

import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException

from .consts import ADDRESS_FORMAT, BODY_STYLE, CARS_TOKEN, CITY, CURR_DATE, DATE_FMT, HEADERS, LAT, \
    LISTING_ID, LNG, MAKE, MILEAGE, MODEL, NAME, PHONE_NUMBER, PRICE, SELLER, STATE, STREET_ADDRESS, TRIM, \
    VIN, YEAR
from ..utils.misc import locate, send_slack_message

logger = getLogger(__name__)


def update_vehicle(vehicle, api):
    """
    Updates vehicle's last date and duration if it exists in the database, creates a new vehicle if it doesn't.
    Updates vehicle's price/seller/mileage if a change is found from the existing price/seller.

    Args:
        vehicle (dict): vehicle to be created/updated
        api (pscraper.api.PscraperAPI): Pscraper api, that allows retrieval/creation of marketplaces

    """
    seller_id = get_seller_id(vehicle, api)
    if seller_id == -1:
        return

    # Post to history table
    api.history_post(vin=vehicle[VIN], price=vehicle[PRICE], seller=seller_id, date=CURR_DATE, mileage=vehicle[MILEAGE])

    # Look for existing VIN
    db_vehicles = api.vehicle_get(vin=vehicle[VIN])
    if db_vehicles == -1:
        return
    elif len(db_vehicles) == 1:
        # Vehicle exists, update data
        db_vehicle = db_vehicles[0]
        get_date = datetime.strptime
        payload = {
            'last_date': CURR_DATE,
            'duration': (get_date(CURR_DATE, DATE_FMT) - get_date(db_vehicle['first_date'], DATE_FMT)).days
        }
        if db_vehicle['mileage'] != vehicle[MILEAGE]:
            payload['mileage'] = vehicle[MILEAGE]
        if db_vehicle['price'] != vehicle[PRICE]:
            payload['price'] = vehicle[PRICE]
        if db_vehicle['seller'] != seller_id:
            payload['seller'] = seller_id

        api.vehicle_patch(vin=vehicle[VIN], **payload)
        return

    # New vehicle, add it to the table
    payload = {
        'first_date': CURR_DATE,
        'last_date': CURR_DATE,
        'duration': 0,
        'listing_id': vehicle[LISTING_ID],
        'vin': vehicle[VIN],
        'make': vehicle[MAKE],
        'model': vehicle[MODEL],
        'body_style': vehicle[BODY_STYLE],
        'price': vehicle[PRICE],
        'trim': vehicle[TRIM],
        'mileage': vehicle[MILEAGE],
        'year': vehicle[YEAR],
        'seller': seller_id,
    }
    api.vehicle_post(**payload)


def get_seller_id(vehicle, api):
    """
    Returns a seller id (primary_key). Search for existing seller by address.
    If not found creates a new seller and returns its id.
    Requires `seller` to have `streetAddress`, `city` and `state`. If any are missing returns -1.

    Args:
        vehicle (dict): Vehicle whose seller needs to be created/searched
        api (pscraper.api.PscraperAPI): Pscraper api, that allows retrieval/creation of marketplaces
    """
    seller = vehicle[SELLER]
    try:
        address = ADDRESS_FORMAT.format(seller[STREET_ADDRESS], seller[CITY], seller[STATE])
    except KeyError:
        address = seller[NAME]

    # Search for existing seller
    db_seller = api.seller_get(address=address)
    if db_seller == -1:
        return -1
    elif len(db_seller) == 1:
        return db_seller[0]['id']

    # New seller, add it to sellers table
    location = seller if LAT in seller and LNG in seller else locate(address, lat_lng_only=True)
    payload = {
        'phone_number': seller[PHONE_NUMBER],
        'name': seller[NAME],
        'address': address,
        'latitude': location[LAT],
        'longitude': location[LNG],
    }
    new_seller = api.seller_post(**payload)
    return new_seller['id'] if new_seller != -1 else -1


def get_cars_com_resp(url):
    """ Scrapes vehicle and page information from cars.com `url`

    Args:
        url (str): Url to get the data from

    Returns:
        (dict): Parsed data about the url and the vehicles it contains
    """
    max_tries, count = 3, 1
    while count <= max_tries:
        try:
            count += 1
            resp = requests.get(url, headers=HEADERS)
            soup = BeautifulSoup(resp.text, 'html.parser')
            val = soup.select('head > script')[2].contents[0]
            return json.loads(val[val.index(CARS_TOKEN) + len(CARS_TOKEN):][:-2])
        except (AttributeError, RequestException, IndexError) as error:
            if count == max_tries:
                logger.critical('cars.com response error', exc_info=error)
                send_slack_message(text=f'cars.com response error: \n{error}')
                return {}
            else:
                logger.info('Retrying cars.com')


def get_autotrader_resp(url):
    """ Scrapes vehicle and page information from autotrader `url`

    Args:
        url (str): Url to get the data from

    Returns:
        (dict): Parsed data about the url and the vehicles it contains
    """
    max_tries, count = 3, 1
    while count <= max_tries:
        try:
            count += 1
            resp = requests.get(url, headers=HEADERS)
            soup = BeautifulSoup(resp.text, 'html.parser').find_all('script', {'type': 'text/javascript'})
            return json.loads(soup[3].contents[0][23:])
        except (AttributeError, RequestException, IndexError) as error:
            if count == max_tries:
                logger.critical('Autotrader response error', exc_info=error)
                send_slack_message(text=f'Autotrader response error: \n{error}')
                return {}
            else:
                logger.info('Retrying cars.com')
