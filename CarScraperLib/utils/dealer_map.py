import csv

import folium
import requests

from .data_io import get_master_table
from ..consts import GOOGLE_MAPS_REQUEST_URL, NOT_APPLICABLE


def build_map(master_table_loc, dealers_geolocation_loc, dealer_map_loc, gcp_api_key):
    """
    :param master_table_loc: path of the master table excel file
    :param dealers_geolocation_loc: path of the dealer geolocation csv file
    :param dealer_map_loc: path where the dealer map will be saved
    :param gcp_api_key: GCP api key to be used for address geo-locations
    :return:
    """
    try:
        dealer_dict = _get_dict_dealers(dealers_geolocation_loc)
        _calc_dealer_geolocation(master_table_loc, dealers_geolocation_loc, dealer_dict, gcp_api_key)
        dealers_map = folium.Map(location=[36.7378, -119.7871], zoom_start=7)
        for name, lat_lng in dealer_dict.items():
            folium.Marker(lat_lng, popup=name).add_to(dealers_map)
        dealers_map.save(dealer_map_loc)
    except AttributeError:
        raise AttributeError(f'`{dealers_geolocation_loc}` is empty or corrupted')


def _get_dict_dealers(dealers_geolocation_loc):
    dealer_dict = {}
    with open(dealers_geolocation_loc, 'r') as csv_file:
        for i, row in enumerate(csv.reader(csv_file, delimiter=',')):
            lat, lng = row[1], row[2]
            if i != 0 and lat != NOT_APPLICABLE and lng != NOT_APPLICABLE:
                dealer_dict[row[0]] = (float(lat), float(lng))
    return dealer_dict


def _calc_dealer_geolocation(master_table_loc, dealer_geolocation, dealer_dict, gcp_api_key):
    for car in get_master_table(master_table_loc).values():
        dealer_name = car.dealer.name
        dealer_address = car.dealer.address
        if dealer_name not in dealer_dict.keys():
            try:
                lat, lng = _get_geolocation(gcp_api_key, dealer_address)
                dealer_dict[dealer_name] = [lat, lng]
            except IndexError as _:
                print(f'Geolocation error for dealer: "{dealer_name}" with address: "{dealer_address}"')
    with open(dealer_geolocation, 'w') as my_csv_file:
        my_csv_file.write('Dealer,Lat,Lng\n')
        for name, address in dealer_dict.items():
            my_csv_file.write(f'{name.replace(",", ";")},{address[0]},{address[1]}\n')


def _get_geolocation(gcp_api_key, address):
    resp = requests.get(GOOGLE_MAPS_REQUEST_URL.format(address, gcp_api_key)).json()
    try:
        return resp['results'][0]['geometry']['location']['lat'], resp['results'][0]['geometry']['location']['lng']
    except KeyError:
        return NOT_APPLICABLE, NOT_APPLICABLE
