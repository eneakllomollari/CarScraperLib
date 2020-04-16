import datetime
import functools
import time
from getpass import getuser
from logging import getLogger
from os import environ
from socket import gethostname
from sys import exc_info
from traceback import format_exception

from slack import WebClient

logger = getLogger(__name__)


def get_geolocation(address, session):
    """ Finds latitude and longitude from a human readable address using Google Maps API.
    You need to set the environment variable `GCP_API_TOKEN` to your Google Maps API token

    Args:
        address (str): Human readable address
        session (requests.sessions.Session): Session to use for geolocating

    Returns:
        latitude, longitude (tuple) Lat, Lng found from Google Maps API
    """
    google_maps_query = f'https://maps.googleapis.com/maps/api/geocode/json?' \
                        f'address={address}&key={environ["GCP_API_TOKEN"]}'
    resp = session.get(google_maps_query).json()
    if resp['status'] != 'OK':
        req = google_maps_query.split("&key")[0]
        text = f'```Error locating address: "{address}"\n\nRequest: {req}\n\nResponse: {resp}```'
        logger.debug(f'Error geolocating address: "{address}"')
        send_slack_message(channel='#errors', text=text)
        return None, None
    return resp['results'][0]['geometry']['location']['lat'], resp['results'][0]['geometry']['location']['lng']


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


def send_slack_report(cars_et, cars_total, at_et, at_total, cm_et, cm_total, states, channel='#daily-job'):
    """
    Post scraping report on slack channel `#daily-job`. Need to set the `SLACK_API_TOKEN` environment variable
    to your slack workspace API token. Uses `utils.misc.send_slack_message`.

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
    states = states if states != 'ALL' else 'All States'
    blocks = [
        {
            'type': 'section',
            'text': {
                'type': 'mrkdwn',
                'text': f'*Scraper Report* _{datetime.datetime.now().date()}_'
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
                    'text': f'*Time*:\t{round(cars_et + at_et + cm_et, 2)} sec'
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
                'text': line.format(success if cars_total > 0 else soon, f'{cars_com_link}   ', cars_total, cars_et)
            }
        },
        {
            'type': 'section',
            'text': {
                'type': 'mrkdwn',
                'text': line.format(success if at_total > 0 else soon, f'{autotrader_link}', at_total,
                                    at_et)
            }
        },
        {
            'type': 'section',
            'text': {
                'type': 'mrkdwn',
                'text': line.format(success if cm_total > 0 else soon, f'{carmax_link}\t ', cm_total, cm_et)
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
