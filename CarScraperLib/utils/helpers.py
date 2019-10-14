import csv
import datetime
import yaml

from ..consts import CURR_DATE, DATE_FORMAT


def update_duration_and_history(price_history, dealership_history, car, master_table):
    listing_id = car.listing_id
    car.last_date = CURR_DATE
    car.first_date = master_table[listing_id].first_date if listing_id in master_table.keys() else CURR_DATE
    car.duration = _get_duration(car.first_date, car.last_date)
    if car.first_date != CURR_DATE:
        if master_table[listing_id].price != car.price:
            _save_change(price_history, listing_id, car.price)
        if master_table[listing_id].dealer.name != car.dealer.name:
            _save_change(dealership_history, listing_id, car.dealer.name.replace(',', ';'))
    return car


def load_yaml_file(file_name):
    with open(file_name) as f:
        return yaml.full_load(f)


def _save_change(history_file, car_id, item):
    new_rows_list = []
    flag = False
    with open(history_file, 'r') as csv_file:
        for row in csv.reader(csv_file, delimiter=','):
            curr_id = row[0]
            if car_id == curr_id:
                flag = True
                new_rows_list.extend([*[v for v in row], *[item, CURR_DATE]])
            else:
                new_rows_list.append(row)
    if not flag:
        new_rows_list.append([car_id, item, CURR_DATE])
    _write_list_to_file(new_rows_list, history_file)


def _write_list_to_file(content_list, file_loc):
    with open(file_loc, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(content_list)


def _get_duration(first_date, last_date):
    return (datetime.datetime.strptime(last_date, DATE_FORMAT)
            - datetime.datetime.strptime(first_date, DATE_FORMAT)).days
