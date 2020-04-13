import datetime
from getpass import getuser
from socket import gethostname

from .misc import send_slack_message


def post_daily_slack_report(cars_et, cars_total, at_et, at_total, cm_et, cm_total, states, channel='#daily-job'):
    """
    Post scraping report on slack channel `#daily-job`. You need to set the `SLACK_API_TOKEN` environment variable
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
                    'text': f'*Total Vehicles:*\t{cars_total + at_total + cm_total}'
                },
                {
                    'type': 'mrkdwn',
                    'text': f'*Total Time*:\t{round(cars_et + at_et + cm_et, 2)} sec'
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
