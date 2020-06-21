import logging
from functools import wraps
from json import JSONDecodeError

import requests
from hamcrest import assert_that, is_in
from requests.exceptions import ConnectionError, RequestException

from .misc import get_traceback, send_slack_message

logger = logging.getLogger(__name__)


def request_wrapper(method, success_codes):
    success_codes = [success_codes] if type(success_codes) is int else success_codes

    def decorator(func):
        @wraps(func)
        def wrapper(self, url, *args, **kwargs):
            url = self.get_full_url(url)
            logger.info(f'Req: {method} {url} {args if args else ""}{kwargs if kwargs else ""}')
            try:
                resp = func(self, url, *args, **kwargs)
                logger.info(f'Resp: {resp.status_code} {resp.text}')
                assert_that(resp.status_code, is_in(success_codes), resp.text)
                return resp.json()
            except (RequestException, ConnectionError, AssertionError, JSONDecodeError) as error:
                error_msg = f'{method} {url} failed\n{error}'
                logger.debug(error_msg, exc_info=get_traceback())
                send_slack_message(text=error_msg)
            return -1

        return wrapper

    return decorator


class BaseAPI(object):
    def __init__(self, base_url, token):
        self.base_url = base_url
        self.headers = {'Authorization': f'Token {token}'}

    def get_full_url(self, url):
        return url if 'http' in url else f'{self.base_url}{url}'

    @request_wrapper('GET', 200)
    def get_request(self, url, params):
        return requests.get(url, params=params, headers=self.headers)

    @request_wrapper('POST', [201, 409])
    def post_request(self, url, data):
        return requests.post(url, data=data, headers=self.headers)

    @request_wrapper('PATCH', 200)
    def patch_request(self, url, data):
        return requests.patch(url, data=data, headers=self.headers)
