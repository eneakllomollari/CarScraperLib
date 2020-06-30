import json
import threading
from json.decoder import JSONDecodeError

import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException

from pscraper.utils.misc import measure_time, send_slack_message
from ..consts import AUTOTRADER_OWNER_QUERY, AUTOTRADER_QUERY, BODY_STYLE, CITY, COUNT, DOMAIN, HEADERS, \
    INITIAL_STATE, INVENTORY, LISTING_ID, MAKE, MAX_THREADS, MILEAGE, MODEL, NAME, OWNER, PHONE_NUMBER, PRICE, \
    RESULTS, SELLER, SRP, STATE, STREET_ADDRESS, TRIM, VIN, YEAR
from ..helpers import logger, update_vehicle


@measure_time
def scrape_autotrader():
    seller_dict, total = {}, 0
    results_count = get_autotrader_resp(AUTOTRADER_QUERY.format(0))[INITIAL_STATE][DOMAIN][SRP][RESULTS][COUNT]
    count = round(results_count / 100) if results_count > 100 else 1
    threads = []
    for index in range(count):
        inventory = get_autotrader_resp(AUTOTRADER_QUERY.format(index * 100))[INITIAL_STATE][INVENTORY]
        for vehicle in inventory.values():
            is_valid_vehicle = update_vehicle_keys(vehicle, seller_dict)
            if is_valid_vehicle and len(vehicle[VIN]) == 17:
                thread = threading.Thread(target=update_vehicle, args=(vehicle, 'Autotrader'))
                thread.start()
                threads.append(thread)
                if len(threads) >= MAX_THREADS:
                    for thread in threads:
                        thread.join()
                    threads.clear()
                total += 1
    for thread in threads:
        thread.join()
    return total


def update_vehicle_keys(vehicle, seller_dict):
    if vehicle[OWNER] not in seller_dict:
        location = locate_owner(vehicle[OWNER])
        seller_dict[OWNER] = location
        if location:
            vehicle[SELLER] = location
        else:
            return False
    try:
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


def locate_owner(owner_id):
    try:
        resp = requests.get(f'{AUTOTRADER_OWNER_QUERY}{owner_id}', headers=HEADERS)
        soup = BeautifulSoup(resp.text, 'html.parser')
        val = soup.find_all('script', {'type': 'application/ld+json', 'data-rh': 'true'})[0].contents[0]
        owner = json.loads(val)
        return {
            NAME: owner['name'],
            PHONE_NUMBER: owner['telephone'],
            STREET_ADDRESS: owner['address']['streetAddress'],
            CITY: owner['address']['addressLocality'],
            STATE: owner['address']['addressRegion'],
        }
    except (AttributeError, KeyError, IndexError, JSONDecodeError, RequestException):
        return {}


def get_autotrader_resp(url):
    try:
        resp = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(resp.text, 'html.parser').find_all('script', {'type': 'text/javascript'})
        return json.loads(soup[3].contents[0][23:])
    except (AttributeError, RequestException, IndexError) as error:
        logger.critical('Autotrader response error', exc_info=error)
        send_slack_message(text=f'Autotrader response error: \n{error}')
        return {}
