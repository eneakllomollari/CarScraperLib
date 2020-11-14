from concurrent import futures
from datetime import datetime
from logging import getLogger

from .consts import ADDRESS_FORMAT, BODY_STYLE, CITY, CURR_DATE, DATE_FMT, LAT, \
    LISTING_ID, LNG, MAKE, MILEAGE, MODEL, NAME, PHONE_NUMBER, PRICE, SELLER, STATE, STREET_ADDRESS, TRIM, \
    VIN, YEAR
from ..api import PscraperAPI
from ..utils.misc import send_slack_message

logger = getLogger(__name__)


def update_vehicle(vehicle, marketplace, lock):
    """
    Updates vehicle's last date and duration if it exists in the database, creates a new vehicle if it doesn't.
    Updates vehicle's price/seller/mileage if a change is found from the existing price/seller.

    Args:
        vehicle (dict): vehicle to be created/updated
        marketplace (str): marketplaces name: Autotrader, Cars.com
        lock (threading.Lock): Lock to control synchronizing of threads
    """
    api = PscraperAPI()
    with lock:
        seller_id = get_seller_id(vehicle, api)
    if seller_id == -1:
        return -1

    # Post to history table
    api.history_post(**{
        'vin': vehicle[VIN],
        'price': vehicle[PRICE],
        'seller': seller_id,
        'date': CURR_DATE,
        'mileage': vehicle[MILEAGE],
        'marketplace': marketplace
    })

    # Look for existing VIN
    db_vehicles = api.vehicle_get(marketplace=marketplace, vin=vehicle[VIN])

    if db_vehicles == -1:
        return 0
    elif len(db_vehicles) >= 1:
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

        api.vehicle_patch(marketplace=marketplace, vin=vehicle[VIN], **payload)
        return 0

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
    api.vehicle_post(marketplace=marketplace, **payload)
    return 0


def get_seller_id(vehicle, api):
    seller = vehicle[SELLER]
    try:
        address = ADDRESS_FORMAT.format(seller[STREET_ADDRESS], seller[CITY], seller[STATE])
    except KeyError:
        send_slack_message(text=f'Address error for seller: {seller} and vehicle: {vehicle}')
        return -1

    # Search for existing seller
    db_seller = api.seller_get(address=address)

    if db_seller == -1:
        return -1
    elif len(db_seller) >= 1:
        return db_seller[0]['id']

    # New seller, add it to sellers table
    payload = {
        'phone_number': seller.get(PHONE_NUMBER),
        'name': seller[NAME],
        'address': address,
        'latitude': seller.get(LAT),
        'longitude': seller.get(LNG),
    }
    new_seller = api.seller_post(**payload)
    return new_seller['id'] if new_seller != -1 else -1


def count_futures_total(marketplace_futures):
    return sum([1 if future.result() == 0 else 0 for future in futures.as_completed(marketplace_futures)])
