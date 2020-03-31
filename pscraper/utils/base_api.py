from functools import wraps

import requests
from hamcrest import assert_that, equal_to, is_in

from .misc import get_traceback, send_slack_message


def request_wrapper(method, success_codes):
    def decorator(func):
        @wraps(func)
        def wrapper(self, url, *args, **kwargs):
            url = self.get_full_url(url)
            try:
                resp = func(self, url, *args, **kwargs)
                assert_func = is_in if type(success_codes) is list else equal_to
                assert_that(resp.status_code, assert_func(success_codes), f'```{method} {url} failed with status code: '
                                                                          f'{resp.status_code}\n'
                                                                          f'Request: {args if args else ""}{kwargs}\n'
                                                                          f'Response: {resp.json()}```')
                return resp.json()
            except (requests.exceptions.RequestException, AssertionError):
                send_slack_message(channel='#errors', text=f'```{get_traceback()}```')
            return -1
        return wrapper
    return decorator


class BaseAPI(object):
    def __init__(self, base_url, auth):
        self.base_url = base_url
        self.auth = auth

    def get_full_url(self, url):
        return url if 'http' in url else f'{self.base_url}{url}'

    @request_wrapper('GET', 200)
    def get_request(self, url, data):
        return requests.get(url, data=data, auth=self.auth)

    @request_wrapper('POST', [201, 409])
    def post_request(self, url, data):
        return requests.post(url, data=data, auth=self.auth)

    @request_wrapper('PATCH', 200)
    def patch_request(self, url, data):
        return requests.patch(url, data=data, auth=self.auth)
