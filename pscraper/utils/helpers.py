import csv
import datetime

import yaml

from .._consts import CURR_DATE, DATE_FORMAT


def update_duration_and_history(price_history, seller_history, vehicle, mastertable):
    """Updates the first_date, last_date and duration of `vehicle`

    Args:
        price_history (str): Path of the price history .csv file
        seller_history (str): Path of the dealership history .csv file
        vehicle (Vehicle): Vehicle whose duration and dates will be updated
        mastertable (dict): Dictionary containing all data

    Returns:
        Vehicle: The updated vehicle

    """
    listing_id = vehicle.listing_id
    vehicle.first_date = mastertable[listing_id].first_date if listing_id in mastertable.keys() else CURR_DATE
    vehicle.last_date = CURR_DATE
    vehicle.duration = _get_duration(vehicle.first_date, vehicle.last_date)
    if vehicle.first_date != CURR_DATE:
        if mastertable[listing_id].price != vehicle.price:
            _save_change(price_history, listing_id, vehicle.price)
        if mastertable[listing_id].seller.name != vehicle.seller.name:
            _save_change(seller_history, listing_id, vehicle.seller.name.replace(',', ';'))
    return vehicle


def load_yaml_file(filename):
    """Loads a yaml file into a dictionary

    Args:
        filename (str): path to yaml file

    Returns:
        dict: Dictionary representation of `filename`

    """
    with open(filename) as f:
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
        csv.writer(f).writerows(content_list)


def _get_duration(first_date, last_date):
    return (datetime.datetime.strptime(last_date, DATE_FORMAT)
            - datetime.datetime.strptime(first_date, DATE_FORMAT)).days
