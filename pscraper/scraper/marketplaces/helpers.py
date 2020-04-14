from datetime import datetime
from logging import getLogger

from pscraper.utils.misc import get_geolocation, send_slack_message
from .consts import ADDRESS_FORMAT, BODY_STYLE, CITY, CURR_DATE, DATE_FMT, LISTING_ID, MAKE, MILEAGE, MODEL, NAME, \
    PHONE_NUMBER, PRICE, SELLER, STATE, STREET_ADDRESS, TRIM, VIN, YEAR

logger = getLogger(__name__)


def update_vehicle(vehicle, api, google_maps_session):
    """
    Updates vehicle's last date and duration if it exists in the database, creates a new vehicle if it doesn't.
    Updates vehicle's price/seller if a change is found from the existing price/seller.
    Args:
        vehicle (dict): vehicle to be created/updated
        api (pscraper.api.API): Pscraper api, that allows retrieval/creation of marketplaces
        google_maps_session (requests.sessions.Session): Google Maps Session to use for geolocating seller
    """
    seller_id = get_seller_id(vehicle, api, google_maps_session)
    if seller_id == -1:
        return

    api.history_post(vin=vehicle[VIN], price=vehicle[PRICE], seller=seller_id, date=CURR_DATE)

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
        if db_vehicle['price'] != vehicle[PRICE]:
            payload.update({'price': vehicle[PRICE]})
        if db_vehicle['seller'] != seller_id:
            payload.update({'seller': seller_id})

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
    If not found creates a new creates a new seller and returns it's id.
    Requires seller to have streetAddress, city and state. If any are missing returns -1.

    Args:
        vehicle(dict): Vehicle whose seller needs to be created/searched
        api (pscraper.api.API): Pscraper api, that allows retrieval/creation of marketplaces
        session (requests.sessions.Session): Google Maps Session to use for geolocating seller
    """
    seller = vehicle[SELLER]
    try:
        address = ADDRESS_FORMAT.format(seller[STREET_ADDRESS], seller[CITY], seller[STATE])
    except KeyError:
        logger.debug(f'Address could not be composed for seller: "{seller}", vehicle: "{vehicle}"')
        send_slack_message(channel='#errors', text=f'```Seller Error:\n{seller}```')
        return -1

    # Search the seller by phone_number
    db_seller = api.seller_get(address=address)
    if db_seller == -1:
        return -1
    elif len(db_seller) >= 1:
        if len(db_seller) > 1:
            logger.debug(f'Found {len(db_seller)} sellers with address: "{address}". Sellers: "{db_seller}"')
        return db_seller[0]['id']

    latitude, longitude = get_geolocation(address, session)
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
