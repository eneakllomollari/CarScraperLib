import functools
import time
from os import environ
from sys import exc_info
from traceback import format_exception

import requests
from slack import WebClient


def get_traceback():
    exc_type, exc_value, exc_traceback = exc_info()
    text = '=' * 80 + '\n'
    for val in format_exception(exc_type, exc_value, exc_traceback):
        text += val
    return '=' * 80 + '\n'


def send_slack_message(**kwargs):
    """ Sends a message in Slack. If only one argument is provided (channel) is provided it sends traceback information
    for debugging. You need to set the `SLACK_API_TOKEN` environment variable to your slack workspace API token

    Args:
        kwargs: Keyword arguments to be used as payload for WebClient
    """
    if len(kwargs) == 1:
        kwargs.update({'text': get_traceback()})
    client = WebClient(token=environ['SLACK_API_TOKEN'])
    client.chat_postMessage(**kwargs)


def get_geolocation(address):
    """ Finds latitude and longitude from a human readable address using Google Maps API.
    You need to set the environment variable `GCP_API_TOKEN` to your Google Maps API token

    Args:
        address (str): Human readable address

    Returns:
        latitude, longitude (tuple) Lat, Lng found from Google Maps API
    """
    google_maps_query = f'https://maps.googleapis.com/maps/api/geocode/json?' \
                        f'address={address}&key={environ["GCP_API_TOKEN"]}'
    resp = requests.get(google_maps_query).json()
    try:
        return resp['results'][0]['geometry']['location']['lat'], \
               resp['results'][0]['geometry']['location']['lng']
    except KeyError:
        return None, None


def measure_time(func):
    """
    A decorator to call a function and track the time spent inside
    Args:
        func: Function to be decorated
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        retval = func(*args, **kwargs)
        end_time = time.time()
        return round(end_time - start_time, 4), retval

    return wrapper
