from requests.sessions import Session

from pscraper.utils.misc import measure_time
from ..consts import CARS_COM_QUERY, LISTING_ID, PAGE, PHONE_NUMBER, SEARCH, SELLER, STATE, TOTAL_NUM_PAGES, VEHICLE, \
    VIN
from ..helpers import get_cars_com_response, update_vehicle, validate_params


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
    validate_params(search_radius, target_states)
    total = 0
    url = CARS_COM_QUERY.format('{}', search_radius, zip_code)
    cars_session, google_maps_session = Session(), Session()
    num_pages = get_cars_com_response(url.format(1), cars_session)[PAGE][SEARCH][TOTAL_NUM_PAGES]
    for i in range(num_pages):
        vehicles = get_cars_com_response(url.format(i), cars_session)[PAGE][VEHICLE]
        for vehicle in vehicles:
            is_eligible_vehicle = all((vehicle[VIN], vehicle[LISTING_ID], vehicle[SELLER][PHONE_NUMBER]))
            is_target_state = vehicle[SELLER][STATE] in target_states
            if is_eligible_vehicle and is_target_state:
                update_vehicle(vehicle, api, google_maps_session)
                total += 1
    return total
