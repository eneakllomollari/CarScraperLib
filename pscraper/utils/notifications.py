from datetime import datetime
from email.mime.text import MIMEText
from os import getenv
from smtplib import SMTP
from sys import exc_info
from traceback import format_exception

from slack import WebClient

from .._consts import DATE_FORMAT

NOTIFICATIONS = 'notifications'
SLACK = 'slack'
EMAIL = 'email'
SENDER = 'sender'
RECEIVERS = 'receivers'
SUCCESS_MESSAGE = 'success_message'


def notify(config, message=None, is_failure=False):
    """Sends a notification as detailed in configuration. Please check `send_email` and `send_slack_message`
    for additional information and requirements.

    Args:
        config (dict): Configuration information for sending the notification
        message (str): Message to send to receivers, defaults to None for traceback information
        is_failure (bool): If set to True receivers get traceback information for debugging

    """
    message, notifications = config[SUCCESS_MESSAGE] if not is_failure else message, config[NOTIFICATIONS]
    if SLACK in notifications:
        send_slack_message(notifications[SLACK][SENDER], notifications[SLACK][RECEIVERS], message)
    if EMAIL in notifications:
        send_email(notifications[EMAIL][SENDER], notifications[EMAIL][RECEIVERS], message)


def send_email(sender, receivers, message=None):
    """Sends an email. If message is `None` it sends traceback information for debugging. Make sure you have
    set the `SENDER_EMAIL_PASSWORD` environment variable to sender's password

    Args:
        sender (str): Sender email
        receivers (list): List of emails that will receive the message
        message (str): Message to be sent, if `None` message contains debugging information

    """
    msg = MIMEText(_get_exception() if message is None else message)
    msg['Subject'] = '[Scraper ALERT] {}!'.format(
        datetime.now().strftime(DATE_FORMAT))
    msg['From'] = 'PHEV Vehicle Scraper'
    msg['To'] = 'PHEV Vehicle Scraper'

    s = SMTP('smtp.gmail.com', 587)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(sender.split('@')[0], getenv('SENDER_EMAIL_PASSWORD'))
    s.sendmail(sender, receivers, msg.as_string())
    s.quit()


def send_slack_message(sender, receivers, message=None):
    """ Sends a message in Slack. If message is None it sends traceback information for debugging. Make sure
    you have set the `SLACK_API_TOKEN` environment variable to your slack workspace API token

    Args:
        sender (str): Sender name
        receivers (list): List of channels that will receive the message
        message (str): Message to be sent, if None message contains debugging information

    """
    text = _get_exception() if message is None else message
    client = WebClient(token=getenv('SLACK_API_TOKEN'))
    for receiver in receivers:
        client.chat_postMessage(channel=receiver, text=text, username=sender)


def _get_exception():
    exc_type, exc_value, exc_traceback = exc_info()
    msg_body = '=' * 80 + '\n'
    for val in format_exception(exc_type, exc_value, exc_traceback):
        msg_body = f'{msg_body}{val}'
    return f'{msg_body}{"=" * 80}\n'
