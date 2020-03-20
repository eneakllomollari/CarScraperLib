from os import environ
from sys import exc_info
from traceback import format_exception

import requests
from slack import WebClient


def send_slack_message(receiver, text=None):
    """ Sends a message in Slack. If message is None it sends traceback information for debugging.
    You need to set the `SLACK_API_TOKEN` environment variable to your slack workspace API token

    Args:
        receiver (str): Channel that will receive the message
        text (str): Message to be sent, if None message will contain debugging information

    """
    if text is None:
        exc_type, exc_value, exc_traceback = exc_info()
        text = '=' * 80 + '\n'
        for val in format_exception(exc_type, exc_value, exc_traceback):
            text = f'{text}{val}'
        text = f'{text}{"=" * 80}\n'

    client = WebClient(token=environ['SLACK_API_TOKEN'])
    client.chat_postMessage(channel=receiver, text=text)


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
