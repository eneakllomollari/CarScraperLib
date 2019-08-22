import csv
import datetime
import logging

from ..constants.consts import DATE_FORMAT

logger = logging.getLogger(__name__)


def calculate_duration_and_history(price_history_file, dealership_history_file, car, master_table):
    listing_id = car.listing_id
    price = car.price
    dealer_name = car.dealer.name
    curr_date = datetime.datetime.now().strftime(DATE_FORMAT)
    car.last_date = curr_date
    if listing_id in master_table.keys():
        car.first_date = master_table[listing_id].first_date

        if master_table[listing_id].price != price:
            _register_price_change(price_history_file, listing_id, price)
        if master_table[listing_id].dealer.name != dealer_name:
            _register_dealer_change(dealership_history_file, listing_id, dealer_name)
    else:
        car.first_date = curr_date

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


def configure_logger(log_path):
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(name)s: \t %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        filename=log_path,
    )


def _register_price_change(price_history_file, car_id, price):
    logger.info(f'\t\t Registering price change to {price} for car id: {car_id}')
    new_rows_list = []
    flag = False
    curr_date = datetime.datetime.now().strftime(DATE_FORMAT)

    with open(price_history_file, 'r') as csv_file:
        for row in csv.reader(csv_file, delimiter=','):
            curr_id = row[0]
            if car_id == curr_id:
                flag = True

                new_row = [v for v in row]
                new_row.append(price)
                new_row.append(curr_date)

                new_rows_list.append(new_row)
            else:
                new_rows_list.append(row)
    if not flag:
        new_rows_list.append([car_id, price, curr_date])
    _write_list_to_file(new_rows_list, price_history_file)


def _register_dealer_change(dealership_history_file, car_id, dealer):
    logger.info(f'\t\t Registering dealer change to {dealer} for car id: {car_id}')
    new_rows_list = []
    dealer = dealer.replace(',', ';')
    flag = False
    curr_date = datetime.datetime.now().strftime(DATE_FORMAT)

    with open(dealership_history_file, 'r') as csv_file:

        for row in csv.reader(csv_file, delimiter=','):
            curr_id = row[0]
            if car_id == curr_id:
                flag = True

                new_row = [v for v in row]
                new_row.append(dealer)
                new_row.append(curr_date)

                new_rows_list.append(new_row)
            else:
                new_rows_list.append(row)

    if not flag:
        row = [curr_id, dealer, curr_date]
        new_rows_list.append(row)
    _write_list_to_file(new_rows_list, dealership_history_file)


def _write_list_to_file(content_list, file_loc):
    with open(file_loc, 'w') as file2:
        writer = csv.writer(file2)
        writer.writerows(content_list)
