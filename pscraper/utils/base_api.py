import logging
from functools import wraps
from json import JSONDecodeError

from hamcrest import assert_that, equal_to, is_in
from requests.exceptions import ConnectionError, RequestException
from requests.sessions import Session

from .misc import get_traceback, send_slack_message

logger = logging.getLogger(__name__)


def request_wrapper(method, success_codes):
    def decorator(func):
        @wraps(func)
        def wrapper(self, url, *args, **kwargs):
            url = self.get_full_url(url)
            logger.info(f'Req: {method} {url} {args if args else ""}{kwargs if kwargs else ""}')
            try:
                resp = func(self, url, *args, **kwargs)
                logger.info(f'Resp: {resp.status_code} {resp.text}')
                assert_func = is_in if type(success_codes) is list else equal_to
                error_msg = f'```{method} {url} failed with status code: {resp.status_code}\n' \
                            f'Req: {args if args else ""}{kwargs}\nResp: {resp.json()}'
                assert_that(resp.status_code, assert_func(success_codes), error_msg)
                return resp.json()
            except (RequestException, ConnectionError, AssertionError, JSONDecodeError):
                logger.debug(f'{method} {url} failed!', exc_info=get_traceback())
                send_slack_message(channel='#errors')
            return -1

        return wrapper

    return decorator


class BaseAPI(object):
    def __init__(self, base_url, token):
        self.base_url = base_url
        self.session = Session()
        self.session.headers.update({'Authorization': f'Token {token}'})

    def get_full_url(self, url):
        return url if 'http' in url else f'{self.base_url}{url}'

    @request_wrapper('GET', 200)
    def get_request(self, url, params):
        return self.session.get(url, params=params)

    @request_wrapper('POST', [201, 409])
    def post_request(self, url, data):
        return self.session.post(url, data=data)

    @request_wrapper('PATCH', 200)
    def patch_request(self, url, data):
        return self.session.patch(url, data=data)
