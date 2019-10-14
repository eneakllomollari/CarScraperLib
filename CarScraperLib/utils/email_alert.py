import datetime
import smtplib
import sys
import traceback
from email.mime.text import MIMEText

from ..consts import DATE_FORMAT


def send_email_with_traceback_info(sender, receivers):
    msg = MIMEText(_get_msg_body())
    msg['Subject'] = f'[PHEV Vehicle Scraper ALERT] {datetime.datetime.now().strftime(DATE_FORMAT)}!'
    msg['From'] = 'PHEV Vehicle Scraper'
    msg['To'] = 'PHEV Vehicle Scraper'

    s = smtplib.SMTP('smtp.gmail.com:587')
    s.ehlo()
    s.starttls()
    s.login(sender['email'].split('@')[0], sender['password'])
    s.sendmail(sender['email'], receivers, msg.as_string())
    s.quit()


def _get_msg_body():
    exc_type, exc_value, exc_traceback = sys.exc_info()
    error_str = '=' * 80 + '\n'
    for val in traceback.format_exception(exc_type, exc_value, exc_traceback):
        error_str += val
    error_str += '=' * 80 + '\n'
    return error_str
