import json

from requests.sessions import Session

from pscraper.utils.misc import geolocate, measure_time
from ..consts import AUTOTRADER_QUERY, BODY_STYLE, COUNT, DOMAIN, INITIAL_STATE, INVENTORY, LISTING_ID, \
    MILEAGE, NAME, OWNER_NAME, PHONE_NUMBER, PRICE, RESULTS, SELLER, SRP, STATE
from ..helpers import get_autotrader_resp, update_vehicle, validate_search_params


@measure_time
def scrape_autotrader(zip_code, search_radius, target_states, api):
    validate_search_params(search_radius, target_states)
    seller_dict, total = {}, 0
    at_session, gm_session = Session(), Session()
    url = AUTOTRADER_QUERY.format(search_radius, zip_code, '{}')
    count = get_autotrader_resp(url.format(0), at_session)[INITIAL_STATE][DOMAIN][SRP][RESULTS][COUNT]
    for index in range(round(count / 100)):
        inventory = get_autotrader_resp(url.format(index * 100), at_session)[INITIAL_STATE][INVENTORY]
        for vehicle in inventory.values():
            if vehicle[OWNER_NAME] not in seller_dict:
                seller_dict[OWNER_NAME] = geolocate(vehicle[OWNER_NAME], gm_session)
            if seller_dict[OWNER_NAME][STATE] in target_states:
                update_vehicle_keys(vehicle, seller_dict[OWNER_NAME])
                update_vehicle(vehicle, api, gm_session)
                total += 1
    return total


def update_vehicle_keys(vehicle, seller):
    with open('vehicle.json', 'w') as fd:
        fd.write(json.dumps(vehicle))

    pricing_detail = vehicle['pricingDetail']
    mileage = vehicle['specifications']['mileage']

    vehicle[LISTING_ID] = vehicle['id']
    vehicle[MILEAGE] = int(mileage['value'].replace(',', '')) if 'value' in mileage else None
    if 'salePrice' in pricing_detail and pricing_detail['salePrice'] != 0:
        vehicle[PRICE] = pricing_detail['salePrice']
    elif 'primary' in pricing_detail:
        vehicle[PRICE] = pricing_detail['primary']
    else:
        vehicle[PRICE] = None
    try:
        vehicle[BODY_STYLE] = ', '.join(vehicle['style'])
    except KeyError:
        vehicle[BODY_STYLE] = None
    try:
        seller[PHONE_NUMBER] = vehicle['phone']['value']
    except KeyError:
        seller[PHONE_NUMBER] = None
    seller[NAME] = vehicle['ownerName']
    vehicle[SELLER] = seller
