import csv
import datetime
import logging

from consts import CURR_DATE, DATE_FORMAT, DEALERSHIP_HISTORY, \
    PRICE_HISTORY, LOG_PATH

logger = logging.getLogger(__name__)


def calculate_duration_and_history(car, master_table):
    listing_id = car.listing_id
    price = car.price
    dealer_name = car.dealer.name
    car.last_date = CURR_DATE().strftime(DATE_FORMAT)
    if listing_id in master_table.keys():
        car.first_date = master_table[listing_id].first_date

        if master_table[listing_id].price != price:
            register_price_change(listing_id, price)
        if master_table[listing_id].dealer.name != dealer_name:
            register_dealer_change(listing_id, dealer_name)
    else:
        car.first_date = CURR_DATE().strftime(DATE_FORMAT)

    car.duration = (
            datetime.date(
                int(car.last_date[6:]),
                int(car.last_date[0:2]),
                int(car.last_date[3:5])
            )
            -
            datetime.date(
                int(car.first_date[6:]),
                int(car.first_date[0:2]),
                int(car.first_date[3:5])
            )
    ).days
    return car


def register_price_change(car_id, price):
    logger.info(f'\t\t Registering price change to {price} for car id: {car_id}')
    new_rows_list = []
    flag = False

    with open(PRICE_HISTORY, 'r') as csv_file:
        for row in csv.reader(csv_file, delimiter=','):
            curr_id = row[0]
            if car_id == curr_id:
                flag = True

                new_row = [v for v in row]
                new_row.append(price)
                new_row.append(CURR_DATE().strftime(DATE_FORMAT))

                new_rows_list.append(new_row)
            else:
                new_rows_list.append(row)
    if not flag:
        new_rows_list.append([car_id, price, CURR_DATE().strftime(DATE_FORMAT)])
    write_list_to_file(new_rows_list, PRICE_HISTORY)


def register_dealer_change(car_id, dealer):
    logger.info(f'\t\t Registering dealer change to {dealer} for car id: {car_id}')
    new_rows_list = []
    dealer = dealer.replace(',', ';')
    flag = False

    with open(DEALERSHIP_HISTORY, 'r') as csv_file:
        for row in csv.reader(csv_file, delimiter=','):
            curr_id = row[0]
            if car_id == curr_id:
                flag = True

                new_row = [v for v in row]
                new_row.append(dealer)
                new_row.append(CURR_DATE().strftime(DATE_FORMAT))

                new_rows_list.append(new_row)
            else:
                new_rows_list.append(row)

    if not flag:
        row = [curr_id, dealer, CURR_DATE().strftime(DATE_FORMAT)]
        new_rows_list.append(row)
    write_list_to_file(new_rows_list, DEALERSHIP_HISTORY)


def write_list_to_file(content_list, file_loc):
    with open(file_loc, 'w') as file2:
        writer = csv.writer(file2)
        writer.writerows(content_list)


def configure_logger():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(name)s: \t %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        filename=LOG_PATH,
    )
