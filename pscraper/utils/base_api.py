import json
from functools import wraps

import requests
from hamcrest import assert_that, equal_to, is_in


def request_wrapper(method, success_codes):
    def decorator(func):
        @wraps(func)
        def wrapper(self, url, *args, **kwargs):
            url = self.get_full_url(url)
            resp = func(self, url, *args, **kwargs)
            assertion_method = is_in if type(success_codes) is list else equal_to
            assert_that(resp.status_code, assertion_method(success_codes),
                        f'{method} {url} failed with status code: {resp.status_code}\n{resp.content}\n{args}{kwargs}')
            return json.loads(resp.content)
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
