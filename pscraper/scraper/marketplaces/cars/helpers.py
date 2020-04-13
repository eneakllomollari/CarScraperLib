import json

from bs4 import BeautifulSoup
from hamcrest import assert_that, equal_to, is_in

from .consts import ALLOWED_RD
from ..consts import STATES


def get_cars_com_response(url, session):
    token = 'CARS.digitalData = '
    for val in BeautifulSoup(session.get(url).text, 'html.parser').find('head').find_all('script'):
        val = val.text.strip()
        try:
            return json.loads(val[val.index(token) + len(token):][:-1])
        except ValueError:
            pass
    raise ValueError(f'cars.com response data was not found!\n\t{url}')


def validate_params(search_radius, target_states):
    """
    Validates that `target_states` are eligible states
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
