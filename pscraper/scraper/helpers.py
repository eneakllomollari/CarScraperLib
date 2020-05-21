import json
from datetime import datetime
from logging import getLogger

from bs4 import BeautifulSoup
from hamcrest import assert_that, is_in
from pscraper.utils.misc import geolocate, send_slack_message

from pscraper.scraper.consts import ADDRESS_FORMAT, ALLOWED_RD, BODY_STYLE, CITY, CURR_DATE, DATE_FMT, HEADERS, LISTING_ID, MAKE, \
    MILEAGE, MODEL, NAME, PHONE_NUMBER, PRICE, SELLER, STATE, STATES, STREET_ADDRESS, TRIM, VIN, YEAR

logger = getLogger(__name__)


def update_vehicle(vehicle, api, google_maps_session):
    """
    Updates vehicle's last date and duration if it exists in the database, creates a new vehicle if it doesn't.
    Updates vehicle's price/seller/mileage if a change is found from the existing price/seller.
    Args:
        vehicle (dict): vehicle to be created/updated
        api (pscraper.api.PscraperAPI): Pscraper api, that allows retrieval/creation of marketplaces
        google_maps_session (requests.sessions.Session): Google Maps Session to use for geolocating seller
    """
    validate_vehicle_keys(vehicle)
    seller_id = get_seller_id(vehicle, api, google_maps_session)
    if seller_id == -1:
        return

    api.history_post(vin=vehicle[VIN], price=vehicle[PRICE], seller=seller_id, date=CURR_DATE, mileage=vehicle[MILEAGE])

    db_vehicles = api.vehicle_get(vin=vehicle[VIN])
    if db_vehicles == -1:
        return
    elif len(db_vehicles) == 1:
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
    else:
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


def get_seller_id(vehicle, api, session):
    """
    Returns a seller id (primary_key). Search for existing seller by address.
    If not found creates a new seller and returns its id.
    Requires `seller` to have `streetAddress`, `city` and `state`. If any are missing returns -1.

    Args:
        vehicle (dict): Vehicle whose seller needs to be created/searched
        api (pscraper.api.PscraperAPI): Pscraper api, that allows retrieval/creation of marketplaces
        session (requests.sessions.Session): Google Maps Session to use for geolocating seller
    """
    seller = vehicle[SELLER]
    try:
        address = ADDRESS_FORMAT.format(seller[STREET_ADDRESS], seller[CITY], seller[STATE])
    except KeyError:
        logger.debug(f'Address could not be composed for seller: "{seller}", vehicle: "{vehicle}"')
        send_slack_message(channel='#errors', text=f'```Seller Error:\n{seller}```')
        return -1

    # Search the seller by address
    db_seller = api.seller_get(address=address)
    if db_seller == -1:
        return -1
    elif len(db_seller) >= 1:
        if len(db_seller) > 1:
            logger.debug(f'Found {len(db_seller)} sellers with address: "{address}". Sellers: "{db_seller}"')
        return db_seller[0]['id']

    latitude, longitude = geolocate(address, session)
    payload = {
        'phone_number': seller[PHONE_NUMBER],
        'name': seller[NAME],
        'address': address,
        'latitude': latitude,
        'longitude': longitude
    }
    new_seller = api.seller_post(**payload)
    if new_seller == -1:
        return -1
    return new_seller['id']


def get_cars_com_response(url, session):
    """ Scrapes vehicle and page information from `url`

    Args:
        url (str): Url to get the response from
        session (requests.sessions.Session): Session to use for sending requests

    Returns:
        (dict): Parsed information about the url and the vehicles it contains
    """
    token = 'CARS.digitalData = '
    resp = session.get(url)
    try:
        for val in BeautifulSoup(resp.text, 'html.parser').find('head').find_all('script'):
            val = val.text.strip()
            try:
                return json.loads(val[val.index(token) + len(token):][:-1])
            except ValueError:
                pass
    except AttributeError as error:
        logger.critical(f'cars.com response error!\t{resp.text}', exc_info=error)
        raise error
    raise ValueError(f'cars.com response data was not found!\t{url}')


def get_autotrader_resp(url, session):
    """ Scrapes vehicle and page information from `url`

    Args:
        url (str): Url to get the response from
        session (requests.sessions.Session): Session to use for sending requests

    Returns:
        (dict): Information about the search results scraped from `url`
    """
    resp = session.get(url, headers=HEADERS)
    soup = BeautifulSoup(resp.text, 'html.parser').find_all('script', {'type': 'text/javascript'})
    return json.loads(soup[3].contents[0][23:])


def validate_search_params(search_radius, target_states):
    assert_that(search_radius, is_in(ALLOWED_RD))
    assert_that(set(target_states).issubset(set(STATES)))


def validate_vehicle_keys(vehicle):
    vehicle_keys = VIN, PRICE, MILEAGE, PRICE, LISTING_ID, MAKE, MODEL, BODY_STYLE, TRIM, YEAR, SELLER
    seller_keys = [STREET_ADDRESS, CITY, STATE, PHONE_NUMBER, NAME]
    for key in vehicle_keys:
        assert_that(key, is_in(vehicle))
    for key in seller_keys:
        assert_that(key, is_in(vehicle[SELLER]))
