import json
from logging import getLogger

from bs4 import BeautifulSoup
from hamcrest import assert_that, equal_to, is_in

from .consts import ALLOWED_RD
from ..consts import STATES

logger = getLogger(__name__)


def get_cars_com_response(url, session):
    """ Scrapes vehicle and page information from `url`

    Args:
        url (str): Url to get the response from
        session (requests.sessions.Session): Session to use for sending requests

    Returns:
        (dict): Parsed information about the url and the vehicles it contains
    """
    token = 'CARS.digitalData = '
    resp = session.get(url)
    try:
        for val in BeautifulSoup(resp.text, 'html.parser').find('head').find_all('script'):
            val = val.text.strip()
            try:
                return json.loads(val[val.index(token) + len(token):][:-1])
            except ValueError:
                pass
    except AttributeError as error:
        logger.critical(f'cars.com response error!\t{resp.text}', exc_info=error)
        raise error
    raise ValueError(f'cars.com response data was not found!\t{url}')


def validate_params(search_radius, target_states):
    """
    Validates that `target_states` are eligible states and `search_radius` is valid

    Args:
        search_radius(int): Radius to scrape in
        target_states(list): states provided by the scraper
    """
    assert_that(search_radius, is_in(ALLOWED_RD))
    if type(target_states) is list:
        for state in target_states:
            assert_that(state, is_in(STATES))
    else:
        assert_that(target_states, equal_to('ALL'))
