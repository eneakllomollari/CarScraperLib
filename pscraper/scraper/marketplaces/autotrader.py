from pscraper.utils.misc import get_phone_number, locate, measure_time
from ..consts import AUTOTRADER_QUERY, BODY_STYLE, COUNT, DOMAIN, INITIAL_STATE, INVENTORY, LISTING_ID, MAKE, \
    MILEAGE, MODEL, NAME, OWNER_NAME, PHONE_NUMBER, PRICE, RESULTS, SELLER, SRP, STATE, TRIM, VIN, YEAR
from ..helpers import get_autotrader_resp, update_vehicle


@measure_time
def scrape_autotrader(zip_code, search_radius, target_states, api):
    """ Scrape EV data from Autotrader filtering with the specified parameters

    Args:
        zip_code (str): The zip code to perform the search in
        search_radius (int): The search radius for the specified zip code
        target_states (list): The states to search in (i.e. ```['CA', 'NV']```)
        api (pscraper.api.PscraperAPI): Pscraper API to communicate with the backend

    Returns:
        total (int): Total number of cars scraped
    """
    seller_dict, total = {}, 0
    url = AUTOTRADER_QUERY.format(search_radius, zip_code, '{}')
    count = get_autotrader_resp(url.format(0))[INITIAL_STATE][DOMAIN][SRP][RESULTS][COUNT]
    for index in range(round(count / 100)):
        inventory = get_autotrader_resp(url.format(index * 100))[INITIAL_STATE][INVENTORY]
        for vehicle in inventory.values():
            is_valid_vehicle = update_vehicle_keys(vehicle, seller_dict)
            is_valid_state = seller_dict[OWNER_NAME][STATE] in target_states or seller_dict[OWNER_NAME][STATE] == ''
            is_valid_vin = len(vehicle[VIN]) == 17
            if is_valid_state and is_valid_vehicle and is_valid_vin:
                update_vehicle(vehicle, api)
                total += 1
    return total


def update_vehicle_keys(vehicle, seller_dict):
    if vehicle[OWNER_NAME] not in seller_dict:
        seller_dict[OWNER_NAME] = locate(vehicle[OWNER_NAME])
        seller_dict[OWNER_NAME][NAME] = vehicle[OWNER_NAME]
        vehicle[SELLER] = seller_dict[OWNER_NAME]
    try:
        try:
            vehicle[SELLER][PHONE_NUMBER] = vehicle['phone']['value']
        except KeyError:
            vehicle[SELLER][PHONE_NUMBER] = get_phone_number(vehicle[SELLER]['place_id'])

        vehicle[LISTING_ID] = vehicle['id']
        vehicle[TRIM] = vehicle.get(TRIM)

        mileage = vehicle['specifications']['mileage']
        vehicle[MILEAGE] = int(mileage['value'].replace(',', '')) if 'value' in mileage else None
        vehicle[BODY_STYLE] = ', '.join(vehicle['style']) if 'style' in vehicle else None

        pricing_detail = vehicle['pricingDetail']
        if 'salePrice' in pricing_detail and pricing_detail['salePrice'] != 0:
            vehicle[PRICE] = pricing_detail['salePrice']
        else:
            vehicle[PRICE] = pricing_detail.get('primary')

        for key in [VIN, MAKE, MODEL, YEAR]:
            if key not in vehicle:
                return False
    except KeyError:
        return False
    return True
