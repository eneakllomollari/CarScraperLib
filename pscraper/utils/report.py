import datetime
from getpass import getuser
from socket import gethostname

from .misc import send_slack_message


def post_daily_slack_report(cars_et, cars_total, at_total, at_et, cm_total, cm_et, channel='#daily-job'):
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
        channel: Slack channel to send the report to, default: `#daily-job`
    """
    success, soon = ':heavy_check_mark:', ':interrobang:'
    line = '{}{}\t\t\t\t\t\t`{}` vehicles in `{}` seconds'
    blocks = [
        {
            'type': 'divider'
        },
        {
            'type': 'divider'
        },
        {
            'type': 'section',
            'text': {
                'type': 'mrkdwn',
                'text': f':electric_plug:\t*{datetime.datetime.now().date()} - Scraper Report*\t:electric_plug:'
            }
        },
        {
            'type': 'divider'
        },
        {
            'type': 'section',
            'fields': [
                {
                    'type': 'mrkdwn',
                    'text': f':car:*Total Vehicles:*\t{cars_total + at_total + cm_total}'
                },
                {
                    'type': 'mrkdwn',
                    'text': f':timer_clock:*Total Time*:\t{cars_et + at_et + cm_et} sec'
                }
            ]
        },
        {
            'type': 'divider'
        },
        {
            'type': 'section',
            'text': {
                'type': 'mrkdwn',
                'text': line.format(success if cars_total > 0 else soon, '<cars.com|Cars.com>\t  ', cars_total, cars_et)
            }
        },
        {
            'type': 'section',
            'text': {
                'type': 'mrkdwn',
                'text': line.format(success if at_total > 0 else soon, '<autotrader.com|Autotrader>   ', at_total,
                                    at_et)
            }
        },
        {
            'type': 'section',
            'text': {
                'type': 'mrkdwn',
                'text': line.format(success if cm_total > 0 else soon, '<carmax.com|CarMax>\t\t', cm_total, cm_et)
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
        {
            'type': 'divider'
        },
    ]
    send_slack_message(channel=channel, blocks=blocks)
