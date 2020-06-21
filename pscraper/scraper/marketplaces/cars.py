from pscraper.scraper.consts import CARS_COM_QUERY, LISTING_ID, PAGE, PHONE_NUMBER, SEARCH, SELLER, STATE, \
    TOTAL_NUM_PAGES, VEHICLE, VIN
from pscraper.scraper.helpers import get_cars_com_resp, update_vehicle
from pscraper.utils.misc import measure_time


@measure_time
def scrape_cars(zip_code, search_radius, target_states, api):
    """ Scrape EV data from cars.com filtering with the specified parameters

    Args:
        zip_code (str): The zip code to perform the search in
        search_radius (int): The search radius for the specified zip code
        target_states (list): The states to search in (i.e. ```['CA', 'NV']```)
        api (pscraper.api.PscraperAPI): Pscraper API to communicate with the backend

    Returns:
        total (int): Total number of cars scraped
    """
    total = 0
    url = CARS_COM_QUERY.format('{}', search_radius, zip_code)
    count = get_cars_com_resp(url.format(1))[PAGE][SEARCH][TOTAL_NUM_PAGES]
    for i in range(count):
        vehicles = get_cars_com_resp(url.format(i))[PAGE][VEHICLE]
        for vehicle in vehicles:
            is_valid_vehicle = all((vehicle[VIN], vehicle[LISTING_ID], vehicle[SELLER][PHONE_NUMBER]))
            is_valid_state = vehicle[SELLER][STATE] in target_states
            is_valid_vin = len(vehicle[VIN]) == 17
            if is_valid_vehicle and is_valid_state and is_valid_vin:
                update_vehicle(vehicle, api)
                total += 1
    return total
