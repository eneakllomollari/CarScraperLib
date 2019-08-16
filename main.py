import logging

from consts import CURR_DATE
from util import get_master_table, save_to_spreadsheet, summarize_data, build_map, \
    calculate_duration_and_history, scrape_and_get_cars_list, configure_logger, send_email

logger = logging.getLogger('main')


def main():
    master_table = get_master_table()
    for car in scrape_and_get_cars_list():
        master_table[car.listing_id] = calculate_duration_and_history(car, master_table)
    save_to_spreadsheet(master_table)


if __name__ == '__main__':
    configure_logger()
    try:
        logger.info(f'\t\t\t ======== Scraping Job Started  {CURR_DATE()}  ============')
        main()
        summarize_data()
        build_map()
        logger.info(f'\t\t\t ======== Scraping Job Finished {CURR_DATE()}  ============')
    except Exception:
        logger.error(f'\t\t\t ======== Exception Occurred     {CURR_DATE()}  ============', exc_info=True)
        send_email()
