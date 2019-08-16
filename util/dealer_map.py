import csv
import logging

import folium
import requests

from consts import DEALER_GEOLOCATION, DEALER_MAP, GOOGLE_MAPS_REQUEST_URL, NOT_APPLICABLE, GCP_API_KEY
from . import get_master_table

logger = logging.getLogger(__name__)


def main():
    logger.info('Started: Building map of dealers')
    dealer_dict = get_dict_dealers()
    calc_dealer_geolocation(dealer_dict)
    build_map(dealer_dict)
    logger.info(f'Finished! Map saved at {DEALER_MAP}')


def get_dict_dealers():
    dealer_dict = {}
    with open(DEALER_GEOLOCATION, 'r') as csv_file:
        read_csv = csv.reader(csv_file, delimiter=',')
        for i, row in enumerate(read_csv):
            lat = row[1]
            lng = row[2]
            if i != 0 and lat != NOT_APPLICABLE and lng != NOT_APPLICABLE:
                dealer_dict[row[0]] = [float(lat), float(lng)]
    return dealer_dict


def build_map(dealer_dict):
    dealers_map = folium.Map(location=[36.7378, -119.7871], zoom_start=7)
    for name, lat_lng in dealer_dict.items():
        folium.Marker(lat_lng, popup=name).add_to(dealers_map)
    dealers_map.save(DEALER_MAP)


def calc_dealer_geolocation(dealer_dict):
    for car in get_master_table().values():
        dealer_name = car.dealer.name
        dealer_address = car.dealer.address
        if dealer_name not in dealer_dict.keys():
            logger.info(f'Getting geolocation of new dealer: {dealer_name}')
            try:
                lat, lng = get_geolocation(dealer_address)
                dealer_dict[dealer_name] = [lat, lng]
            except IndexError:
                logger.info(f'Geolocation error for dealer: {dealer_name} with address: {dealer_address}')
    with open(DEALER_GEOLOCATION, 'w') as my_csv_file:
        my_csv_file.write('Dealer Name,Lat,Lng\n')
        for name, add in dealer_dict.items():
            name = name.replace(',', ';')
            my_csv_file.write(f'{name},{add[0]},{add[1]}\n')


def get_geolocation(address):
    with open(GCP_API_KEY, 'r') as api_file:
        api_key = api_file.read().replace('\n', '')
    resp = requests.get(GOOGLE_MAPS_REQUEST_URL.format(address, api_key)).json()
    location = resp['results'][0]['geometry']['location']
    return location['lat'], location['lng']
