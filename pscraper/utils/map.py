import csv
from os import getenv

import folium
import requests

from .io import get_master_table
from .._consts import GOOGLE_MAPS_REQUEST, NOT_APPLICABLE


def build_map(mastertable_path, dealers_geoloc, dealer_map_loc):
    """Builds an html geolocation map of current dealers

    Args:
        mastertable_path (str): Path of the master table excel file
        dealers_geoloc (str): Path of the dealer geolocation csv file
        dealer_map_loc (str): Path where the dealer map will be saved

    """
    try:
        dealer_dict = _get_dict_dealers(dealers_geoloc)
        _calc_dealer_geolocation(mastertable_path, dealers_geoloc, dealer_dict, getenv('GCP_API_TOKEN'))
        dealers_map = folium.Map(location=[36.7378, -119.7871], zoom_start=7)
        for name, lat_lng in dealer_dict.items():
            folium.Marker(lat_lng, popup=name).add_to(dealers_map)
        dealers_map.save(dealer_map_loc)
    except AttributeError as e:
        raise AttributeError(f'`{dealers_geoloc}` is empty or corrupted\n{e}')


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
        name = car.seller.name
        add = car.seller.address
        if name not in dealer_dict.keys():
            try:
                lat, lng = _get_geolocation(gcp_api_key, add)
                dealer_dict[name] = [lat, lng]
            except IndexError:
                print('Geolocation error for dealer: "{}" with address: "{}"'.format(name, add))
    with open(dealer_geolocation, 'w') as my_csv_file:
        my_csv_file.write('Dealer,Lat,Lng\n')
        for name, address in dealer_dict.items():
            my_csv_file.write('{},{},{}\n'.format(name.replace(",", ";"), address[0], address[1]))


def _get_geolocation(gcp_api_key, address):
    resp = requests.get(GOOGLE_MAPS_REQUEST.format(address, gcp_api_key)).json()
    try:
        return resp['results'][0]['geometry']['location']['lat'], \
               resp['results'][0]['geometry']['location']['lng']
    except KeyError:
        return NOT_APPLICABLE, NOT_APPLICABLE
