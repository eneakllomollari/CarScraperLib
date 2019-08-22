import csv
import logging

import folium
import requests

from .data_io import get_master_table
from ..constants.consts import GOOGLE_MAPS_REQUEST_URL, NOT_APPLICABLE

logger = logging.getLogger(__name__)


def build_map(master_table_loc, dealer_geolocation_loc, dealer_map_loc):
    """
    :param master_table_loc: path of the master table excel file
    :param dealer_geolocation_loc: path of the dealer geolocation csv file
    :param dealer_map_loc: path where the dealer map will be saved
    :return:
    """
    dealer_dict = _get_dict_dealers(dealer_geolocation_loc)
    _calc_dealer_geolocation(master_table_loc, dealer_geolocation_loc, dealer_dict)
    dealers_map = folium.Map(location=[36.7378, -119.7871], zoom_start=7)
    for name, lat_lng in dealer_dict.items():
        folium.Marker(lat_lng, popup=name).add_to(dealers_map)
    dealers_map.save(dealer_map_loc)


def _get_dict_dealers(dealer_geolocation):
    dealer_dict = {}
    with open(dealer_geolocation, 'r') as csv_file:
        read_csv = csv.reader(csv_file, delimiter=',')
        for i, row in enumerate(read_csv):
            lat = row[1]
            lng = row[2]
            if i != 0 and lat != NOT_APPLICABLE and lng != NOT_APPLICABLE:
                dealer_dict[row[0]] = [float(lat), float(lng)]
            return dealer_dict


def _calc_dealer_geolocation(master_table_loc, dealer_geolocation, dealer_dict):
    for car in get_master_table(master_table_loc).values():
        dealer_name = car.dealer.name
        dealer_address = car.dealer.address
        if dealer_name not in dealer_dict.keys():
            logger.info(f'Getting geolocation of new dealer: {dealer_name}')
            try:
                lat, lng = _get_geolocation(master_table_loc, dealer_address)
                dealer_dict[dealer_name] = [lat, lng]
            except IndexError:
                logger.info(f'Geolocation error for dealer: {dealer_name} with address: {dealer_address}')
    with open(dealer_geolocation, 'w') as my_csv_file:
        my_csv_file.write('Dealer Name,Lat,Lng\n')
        for name, add in dealer_dict.items():
            name = name.replace(',', ';')
            my_csv_file.write(f'{name},{add[0]},{add[1]}\n')


def _get_geolocation(gcp_api_key, address):
    with open(gcp_api_key, 'r') as api_file:
        api_key = api_file.read().replace('\n', '')
    resp = requests.get(GOOGLE_MAPS_REQUEST_URL.format(address, api_key)).json()
    location = resp['results'][0]['geometry']['location']
    return location['lat'], location['lng']
