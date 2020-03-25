from pscraper.utils.report import post_daily_slack_report
from .autotrader import scrape_autotrader
from .carmax import scrape_carmax
from .cars import scrape_cars


def scrape(zip_code, search_radius, target_states, api):
    """ Scrape data about electric vehicles from all supported marketplaces using the specified parameters
    You need credentials with admin permissions to be set to environment variables
     `PSCRAPER_USERNAME` and `PSCRAPER_PASSWORD`

    Args:
        zip_code (str): The zip code to perform the search in
        search_radius (str): The search radius for the specified zip code
        target_states (list): The states to search in (i.e. ```['CA', 'NV']```)
        api (pscraper.api.API): Pscraper API to communicate with the DB

    Returns:
        total: Number of scraped cars per marketplaces (cars.com, autotrader, carmax)

    """
    cars_et, cars_total = scrape_cars(zip_code, search_radius, target_states, api)
    autotrader_et, autotrader_total = scrape_autotrader(zip_code, search_radius, target_states, api)
    carmax_et, carmax_total = scrape_carmax(zip_code, search_radius, target_states, api)

    post_daily_slack_report(cars_et, cars_total, autotrader_et, autotrader_total, carmax_et, carmax_total)

    return cars_total, autotrader_total, carmax_total
