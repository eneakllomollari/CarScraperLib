import functools
import os
import time
from datetime import datetime, timedelta
from getpass import getuser
from logging import getLogger
from socket import gethostname
from sys import exc_info
from traceback import format_exception
from urllib.parse import quote

import requests
import slack

logger = getLogger(__name__)


def locate(raw_address, lat_lng_only=False):
    """ Geo-locates a human readable address and breaks it down to lat, lng, zip code and address using Google Maps API.
    You need to set the environment variable `GCP_API_TOKEN` to your Google Maps API token

    Args:
        raw_address (str): Human readable address
        lat_lng_only (bool): Include only lat and lng in the return dict

    Returns:
        latitude, longitude (tuple) Lat, Lng found from Google Maps API
    """
    address = {'streetAddress': '', 'city': '', 'state': '', 'lat': '', 'lng': '', 'place_id': ''}
    resp = requests.get(f'https://maps.googleapis.com/maps/api/geocode/json?address={quote(raw_address)}'
                        f'&key={os.getenv("GCP_API_TOKEN")}').json()
    if resp['status'] != 'OK':
        if resp['status'] == 'ZERO_RESULTS':
            return address
        logger.debug(f'Error geolocating address: "{raw_address}"')
        send_slack_message(text=f'Error locating address: "{raw_address}"\nResponse: {resp}')
        return address
    location = resp['results'][0]['geometry']['location']
    address['lat'], address['lng'] = location['lat'], location['lng']
    if lat_lng_only:
        return address
    address['place_id'] = resp['results'][0]['place_id']
    for comp in resp['results'][0]['address_components']:
        if 'street_number' in comp['types']:
            address['streetAddress'] += comp['short_name']
        elif 'route' in comp['types']:
            address['streetAddress'] += ' ' + comp['short_name']
        elif 'locality' in comp['types']:
            address['city'] = comp['short_name']
        elif 'administrative_area_level_1' in comp['types']:
            address['state'] = comp['short_name']
    return address


def get_phone_number(place_id):
    url = f'https://maps.googleapis.com/maps/api/place/details/json?inputtype=textquery&fields=formatted_phone_number' \
          f'&place_id={place_id}&key={os.getenv("GCP_API_TOKEN")}'
    resp = requests.get(url).json()
    try:
        phone_number = resp['result']['formatted_phone_number']
        return phone_number.replace('(', '').replace(')', '').replace(' ', '').replace('-', '')
    except KeyError:
        return ''


def measure_time(func):
    """
    A decorator to call a function and track the time it takes for the function to finish execution

    Args:
        func: Function to be decorated
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        retval = func(*args, **kwargs)
        end_time = time.time()
        return round(end_time - start_time, 1), retval

    return wrapper


def get_traceback():
    """
    Get formatted traceback information after exception

    Returns:
        text (str): Traceback text
    """
    return ''.join([str(val) for val in format_exception(*exc_info())])


def send_slack_message(**kwargs):
    """ Sends a message in Slack. You need to set the `SLACK_API_TOKEN` environment variable of your slack API token

    Args:
        kwargs: Keyword arguments to be used as payload for WebClient
    """
    if 'text' not in kwargs:
        kwargs['text'] = f'```{datetime.now()}:{get_traceback()}```'
    else:
        kwargs['text'] = f'```{datetime.now()}:{kwargs["text"]}```'
    if 'channel' not in kwargs:
        kwargs['channel'] = '#errors'
    if getuser() == 'enea':
        kwargs['channel'] = '#debug'

    client = slack.WebClient(token=os.getenv('SLACK_API_TOKEN'))
    client.chat_postMessage(**kwargs)


def send_slack_report(cars_et, cars_total, at_et, at_total, cm_et, cm_total, states, channel='#daily-job'):
    """
    Post scraping report on slack channel `#daily-job` by default.
    Need to set the `SLACK_API_TOKEN` environment variable to your slack workspace API token.
    Uses `utils.misc.send_slack_message`.

    Args:
        cars_et: Time in seconds it took to scrape cars.com
        cars_total: Number of vehicles scraped from cars.com
        at_total: Time in seconds it took to scrape autotrader
        at_et: Number of vehicles scraped from autotrader
        cm_total: Time in seconds it took to scrape carmax
        cm_et: Number of vehicles scraped from carmax
        states: Scraped states to include in the report
        channel: Slack channel to send the report to, default: `#daily-job`
    """
    success, soon = ':heavy_check_mark:', ':interrobang:'
    line = '{}{}\t\t`{}` vehicles in `{}` sec'
    carmax_link = '<https://www.carmax.com/|CarMax>'
    autotrader_link = '<https://www.autotrader.com/|Autotrader>'
    cars_com_link = '<https://www.cars.com/|Cars.com>'
    blocks = [
        {
            'type': 'section',
            'text': {
                'type': 'mrkdwn',
                'text': f'*Scraper Report* _{datetime.now().date()}_'
            }
        },
        {
            'type': 'section',
            'fields': [
                {
                    'type': 'mrkdwn',
                    'text': f'*Total:*\t{cars_total + at_total + cm_total} vehicles'
                },
                {
                    'type': 'mrkdwn',
                    'text': f'*Time*:\t{_get_duration(cars_et + at_et + cm_et)}'
                },
                {
                    'type': 'mrkdwn',
                    'text': f'*States*:\t{states}'
                }
            ]
        },
        {
            'type': 'section',
            'text': {
                'type': 'mrkdwn',
                'text': line.format(success if cars_total > 0 else soon, f'{cars_com_link}   ', cars_total,
                                    _get_duration(cars_et))
            }
        },
        {
            'type': 'section',
            'text': {
                'type': 'mrkdwn',
                'text': line.format(success if at_total > 0 else soon, f'{autotrader_link}', at_total,
                                    _get_duration(at_et))
            }
        },
        {
            'type': 'section',
            'text': {
                'type': 'mrkdwn',
                'text': line.format(success if cm_total > 0 else soon, f'{carmax_link}\t ', cm_total,
                                    _get_duration(cm_et))
            }
        },
        {
            'type': 'context',
            'elements': [
                {
                    'type': 'mrkdwn',
                    'text': f'{getuser()}@{gethostname()}',
                }
            ]
        },
        {
            'type': 'divider'
        },
    ]
    send_slack_message(channel=channel, blocks=blocks, text='Daily Report')


def _get_duration(seconds):
    return str(timedelta(seconds=seconds)).split(".")[0]
