from requests.sessions import Session

from pscraper.utils.misc import geolocate, measure_time
from ..consts import AUTOTRADER_QUERY, BODY_STYLE, COUNT, DOMAIN, INITIAL_STATE, INVENTORY, LISTING_ID, MILEAGE, \
    OWNER_NAME, PRICE, RESULTS, SRP, STATE
from ..helpers import get_autotrader_resp, update_vehicle, validate_params


@measure_time
def scrape_autotrader(zip_code, search_radius, target_states, api):
    validate_params(search_radius, target_states)
    seller_dict = {}
    at_session, gm_session = Session(), Session()
    url = AUTOTRADER_QUERY.format(search_radius, zip_code, '{}')
    count = get_autotrader_resp(url.format(0), at_session)[INITIAL_STATE][DOMAIN][SRP][RESULTS][COUNT]
    for index in range(round(count / 100)):
        inventory = get_autotrader_resp(url.format(index * 100), at_session)[INITIAL_STATE][INVENTORY]
        for vehicle in inventory.values():
            if vehicle[OWNER_NAME] not in seller_dict:
                seller_dict[OWNER_NAME] = geolocate(vehicle[OWNER_NAME], gm_session)
            if seller_dict[OWNER_NAME][STATE] in target_states:
                normalize_keys(vehicle)
                update_vehicle(vehicle, api, gm_session)


def normalize_keys(vehicle):
    pricing_detail = vehicle['pricingDetail']
    mileage = vehicle['specifications']['mileage']

    vehicle[PRICE] = pricing_detail['salePrice'] if pricing_detail['salePrice'] != 0 else pricing_detail['primary']
    vehicle[MILEAGE] = mileage['value'] if 'value' in mileage else None
    vehicle[LISTING_ID] = vehicle['id']
    vehicle[BODY_STYLE] = ', '.join(vehicle['style'])
