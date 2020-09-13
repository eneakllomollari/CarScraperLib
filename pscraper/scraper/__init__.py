import threading
from concurrent import futures

from .helpers import count_futures_total, update_vehicle
from .marketplaces.autotrader import scrape_autotrader
from .marketplaces.cars import scrape_cars


def pscrape():
    lock = threading.Lock()
    with futures.ThreadPoolExecutor() as executor:
        cars_futures = {executor.submit(update_vehicle, v, 'Cars.com', lock): v for v in scrape_cars()}
        autotrader_futures = {executor.submit(update_vehicle, v, 'Autotrader', lock): v for v in scrape_autotrader()}

        cars_total = count_futures_total(cars_futures)
        autotrader_total = count_futures_total(autotrader_futures)
    return cars_total, autotrader_total
