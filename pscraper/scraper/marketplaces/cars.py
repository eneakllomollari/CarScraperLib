import json
import logging
import threading
from json.decoder import JSONDecodeError

import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException

from pscraper.utils.misc import get_traceback, measure_time, send_slack_message
from ..consts import CARS_COM_QUERY, CARS_TOKEN, CITY, LISTING_ID, PAGE, PHONE_NUMBER, SEARCH, SELLER, STATE, \
    STREET_ADDRESS, TOTAL_NUM_PAGES, VEHICLE, VIN
from ..helpers import update_vehicle

logger = logging.getLogger(__name__)


@measure_time
def scrape_cars():
    threads, lock = [], threading.Lock()
    resp = get_cars_com_resp(CARS_COM_QUERY.format(1))
    if not resp:
        return
    total, num_pages = 0, resp[PAGE][SEARCH][TOTAL_NUM_PAGES]
    for i in range(num_pages):
        vehicles = get_cars_com_resp(CARS_COM_QUERY.format(i))[PAGE][VEHICLE]
        for vehicle in vehicles:
            is_valid_vehicle = all((vehicle[VIN], vehicle[LISTING_ID], vehicle[SELLER][PHONE_NUMBER]))
            is_valid_vin = len(vehicle[VIN]) == 17
            is_valid_seller = all([attr in vehicle[SELLER] for attr in [STREET_ADDRESS, CITY, STATE]])
            if is_valid_vehicle and is_valid_vin and is_valid_seller:
                thread = threading.Thread(target=update_vehicle, args=(vehicle, 'Cars.com', lock))
                thread.start()
                threads.append(thread)
                total += 1
    for thread in threads:
        thread.join()
    return total


def get_cars_com_resp(url):
    try:
        logger.info(f'Getting: {url}')
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text, 'html.parser')
        val = soup.select('head > script')[2].contents[0]
        return json.loads(val[val.index(CARS_TOKEN) + len(CARS_TOKEN):][:-2])
    except (AttributeError, KeyError, IndexError, JSONDecodeError, RequestException):
        logger.critical(f'cars.com response error\n{resp.text}', exc_info=1)
        send_slack_message(text=f'cars.com response error: \n{get_traceback()}')
        return {}
