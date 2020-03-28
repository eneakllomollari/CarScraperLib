from datetime import datetime

from hamcrest import any_of, assert_that, has_length

from pscraper.utils.misc import get_geolocation
from .consts import BODY_STYLE, CITY, CURR_DATE, DATE_FMT, LISTING_ID, MAKE, MILEAGE, MODEL, NAME, PHONE_NUMBER, \
    PRICE, STATE, STREET_ADDRESS, TRIM, VIN, YEAR


def update_vehicle(vehicle, api):
    """
    Updates vehicle's last date and duration if it exists in the database, creates a new vehicle if it doesn't.
    Updates vehicle's price if a change is found from the existing price.
    Args:
        vehicle (dict): vehicle to be created/updated
        api (pscraper.api.API): Pscraper api, that allows retrieval/creation of marketplaces
    """
    db_vehicles = api.vehicle_get(vin=vehicle[VIN], listing_id=vehicle[LISTING_ID], make=vehicle[MAKE],
                                  model=vehicle[MODEL])
    assert_that(db_vehicles, has_length(any_of(0, 1)), db_vehicles)
    if len(db_vehicles) == 1:
        db_vehicle = db_vehicles[0]
        get_date = datetime.strptime
        payload = {
            'last_date': CURR_DATE,
            'duration': (get_date(CURR_DATE, DATE_FMT) - get_date(db_vehicle['first_date'], DATE_FMT)).days
        }
        if db_vehicle['price'] != vehicle[PRICE]:
            payload.update({'price': vehicle[PRICE]})
        api.vehicle_patch(db_vehicle['id'], **payload)
    else:
        payload = {
            'first_date': CURR_DATE,
            'last_date': CURR_DATE,
            'duration': 0,
            'listing_id': vehicle[LISTING_ID],
            'body_style': vehicle[BODY_STYLE],
            'vin': vehicle[VIN],
            'make': vehicle[MAKE],
            'price': vehicle[PRICE],
            'model': vehicle[MODEL],
            'trim': vehicle[TRIM],
            'mileage': vehicle[MILEAGE],
            'year': vehicle[YEAR],
            'seller_id': get_seller_id(vehicle, api),
        }
        api.vehicle_put(payload)


def get_seller_id(seller, api):
    """
    Returns a seller id (primary_key). Search for existing seller by phone number and name.
    If not found creates a new creates a new seller and returns it's id

    Args:
        seller(dict): Seller that needs to be created or updated
        api (pscraper.api.API): Pscraper api, that allows retrieval/creation of marketplaces
    """
    # Search the seller by phone number
    db_sellers_phone = api.seller_get(phone_number=seller[PHONE_NUMBER])
    if len(db_sellers_phone) == 1:
        return db_sellers_phone[0]['id']

    # Search the seller by name
    db_sellers_name = api.seller_get(name=seller[NAME])
    if len(db_sellers_name) == 1:
        return db_sellers_name[0]['id']

    # Seller not found, create a new one
    address = f'{seller[STREET_ADDRESS]}, {seller[CITY]}, {seller[STATE]}'
    latitude, longitude = get_geolocation(address)
    payload = {
        'phone_number': seller[PHONE_NUMBER],
        'name': seller[NAME],
        'address': address,
        'latitude': latitude,
        'longitude': longitude
    }
    new_seller = api.seller_put(payload)
    return new_seller['id']
