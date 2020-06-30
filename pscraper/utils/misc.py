import functools
import os
import time
from datetime import datetime, timedelta
from getpass import getuser
from logging import getLogger
from socket import gethostname
from sys import exc_info
from traceback import format_exception

import slack

logger = getLogger(__name__)


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
    return ''.join([str(val) for val in format_exception(*exc_info())])


def send_slack_message(**kwargs):
    if 'text' not in kwargs:
        kwargs['text'] = f'```{datetime.now()}: {get_traceback()}```'
    else:
        kwargs['text'] = f'```{datetime.now()}: {kwargs["text"]}```'
    if 'channel' not in kwargs:
        kwargs['channel'] = '#errors'
    if getuser() == 'enea':
        kwargs['channel'] = '#debug'

    client = slack.WebClient(token=os.getenv('SLACK_API_TOKEN'))
    client.chat_postMessage(**kwargs)


def send_slack_report(cars, autotrader, states, channel='#daily-job'):
    cars_et, cars_total = cars
    at_et, at_total = autotrader
    success, soon = ':heavy_check_mark:', ':interrobang:'
    line = '{}{}\t\t`{}` vehicles in `{}` sec'
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
                    'text': f'*Total:*\t{cars_total + at_total} vehicles'
                },
                {
                    'type': 'mrkdwn',
                    'text': f'*Time*:\t{_get_duration(cars_et + at_et)}'
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
