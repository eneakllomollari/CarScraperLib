import json

import requests
from hamcrest import assert_that, equal_to, any_of
from requests.auth import HTTPBasicAuth


class API:
    def __init__(self, username, password):
        self.auth = HTTPBasicAuth(username, password)
        self.app = f'http://pscraper.herokuapp.com/pscraper'

    # ===== GET =====
    def seller_get(self, **kwargs):
        resp = requests.get(f'{self.app}/seller/', params=kwargs, auth=self.auth)
        assert_that(resp.status_code, equal_to(200), resp.content)
        return json.loads(resp.content)

    def vehicle_get(self, **kwargs):
        resp = requests.get(f'{self.app}/vehicle/', params=kwargs, auth=self.auth)
        assert_that(resp.status_code, equal_to(200), resp.content)
        return json.loads(resp.content)

    # ===== PUT =====
    def seller_put(self, seller):
        resp = requests.put(f'{self.app}/seller/', data=seller, auth=self.auth)
        assert_that(resp.status_code, any_of(201, 409), resp.content)
        return json.loads(resp.content)

    def vehicle_put(self, vehicle):
        resp = requests.put(f'{self.app}/vehicle/', data=vehicle, auth=self.auth)
        assert_that(resp.status_code, any_of(201, 409), resp.content)
        return json.loads(resp.content)

    # ===== PATCH =====
    def seller_patch(self, primary_key, **kwargs):
        params = {'id': primary_key}
        resp = requests.patch(f'{self.app}/seller/', params=params, data=kwargs, auth=self.auth)
        assert_that(resp.status_code, equal_to(200), resp.content)
        return json.loads(resp.content)

    def vehicle_patch(self, primary_key, **kwargs):
        params = {'id': primary_key}
        resp = requests.patch(f'{self.app}/vehicle/', params=params, data=kwargs, auth=self.auth)
        assert_that(resp.status_code, equal_to(200), resp.content)
        return json.loads(resp.content)
