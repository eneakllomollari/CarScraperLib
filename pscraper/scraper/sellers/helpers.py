import datetime

from hamcrest import assert_that, has_length, any_of

from pscraper.utils import get_geolocation
from .consts import SELLER, STATE, VIN, LISTING_ID, NAME, MAKE, MODEL, PRICE, CITY, \
    PHONE_NUMBER, STREET_ADDRESS, BODY_STYLE, TRIM, MILEAGE, YEAR, DATE_FORMAT


def update_vehicle(vehicle, api):
    """
    Update vehicle's last date and duration if it exists in the database,
    create a new vehicle if it doesn't

    Args:
        vehicle (dict): vehicle to be created/updated
        api (pscraper.api.API): Pscraper api, that allows retrieval/creation of sellers
    """
    db_vehicles = api.vehicle_get(vin=vehicle[VIN], listing_id=vehicle[LISTING_ID],
                                  make=vehicle[MAKE], model=vehicle[MODEL])
    assert_that(db_vehicles, has_length(any_of(0, 1)))
    curr_date = datetime.datetime.now().strftime(DATE_FORMAT)
    if len(db_vehicles) == 1:
        db_vehicle = db_vehicles[0]
        duration = datetime.datetime.strptime(curr_date, DATE_FORMAT) - datetime.datetime.strptime(
            db_vehicle['first_date'], DATE_FORMAT)
        payload = {
            'last_date': curr_date,
            'duration': duration.days
        }
        if db_vehicle['price'] != vehicle[PRICE]:
            payload.update({'price': vehicle[PRICE]})
        api.vehicle_patch(db_vehicle['id'], **payload)
    else:
        payload = {
            'first_date': curr_date,
            'last_date': curr_date,
            'duration': 0,
            'listing_id': vehicle[LISTING_ID],
            'body_style': vehicle[BODY_STYLE],
            'vin': vehicle[VIN],
            'make': vehicle[MAKE],
            'price': vehicle[PRICE] or 0,
            'model': vehicle[MODEL],
            'trim': vehicle[TRIM],
            'mileage': vehicle[MILEAGE],
            'year': vehicle[YEAR],
            'seller_id': vehicle['seller_id'],
        }
        api.vehicle_put(payload)


def update_seller_id(vehicle, api):
    """
    Update `vehicle[SELLER_ID]`. Creates a new seller if seller is not in the database

    Args:
        vehicle (dict): Vehicle's whose seller id needs to be updates
        api (pscraper.api.API): Pscraper api, that allows retrieval/creation of sellers
    """
    seller = vehicle[SELLER]
    db_sellers_phone = api.seller_get(phone_number=seller[PHONE_NUMBER])
    db_sellers_name = api.seller_get(name=seller[NAME])
    assert_that(db_sellers_phone, has_length(any_of(0, 1)))
    assert_that(db_sellers_name, has_length(any_of(0, 1)))
    if len(db_sellers_phone) == 1:
        vehicle['seller_id'] = db_sellers_phone[0]['id']
    elif len(db_sellers_name) == 1:
        vehicle['seller_id'] = db_sellers_name[0]['id']
    else:
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
        vehicle['seller_id'] = new_seller['id']
