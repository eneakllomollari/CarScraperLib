import functools
import time
from os import environ
from sys import exc_info
from traceback import format_exception

from slack import WebClient


def send_slack_message(**kwargs):
    """ Sends a message in Slack. If only one argument is provided (channel) it sends traceback information about
    the most recent exception. You need to set the `SLACK_API_TOKEN` environment variable of your slack workspace
     API token

    Args:
        kwargs: Keyword arguments to be used as payload for WebClient
    """
    if len(kwargs) == 1:
        kwargs.update({'text': f'```{get_traceback()}```'})
    client = WebClient(token=environ['SLACK_API_TOKEN'])
    client.chat_postMessage(**kwargs)


def get_geolocation(address, session):
    """ Finds latitude and longitude from a human readable address using Google Maps API.
    You need to set the environment variable `GCP_API_TOKEN` to your Google Maps API token

    Args:
        address (str): Human readable address

    Returns:
        latitude, longitude (tuple) Lat, Lng found from Google Maps API
    """
    google_maps_query = f'https://maps.googleapis.com/maps/api/geocode/json?' \
                        f'address={address}&key={environ["GCP_API_TOKEN"]}'
    resp = session.get(google_maps_query).json()
    if resp['status'] != 'OK':
        req = google_maps_query.split("&key")[0]
        text = f'```Error locating address: "{address}"\n\nRequest: {req}\n\nResponse: {resp}```'
        send_slack_message(channel='#errors', text=text)
        return None, None
    return resp['results'][0]['geometry']['location']['lat'], resp['results'][0]['geometry']['location']['lng']


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
        return round(end_time - start_time, 1), retval

    return wrapper


def get_traceback():
    """
    Get formatted traceback information after exception
    Returns:
        text(str): Traceback text
    """
    return ''.join([str(val) for val in format_exception(*exc_info())])
