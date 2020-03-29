from pscraper.utils.misc import measure_time
from ..helpers import validate_states


# TODO
@measure_time
def scrape_autotrader(zip_code, search_radius, target_states, api):
    validate_states(target_states)
    return 0
