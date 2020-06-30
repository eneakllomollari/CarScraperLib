import os

from pscraper.utils.base_api import BaseAPI

MARKETPLACE_URLS = {
    'Autotrader': '/autotrader-vehicle/',
    'Cars.com': '/cars-com-vehicle/'
}


class PscraperAPI(BaseAPI):
    """
    Provides the APIs to interact with the pscraper backend application
    """

    def __init__(self):
        host = os.getenv('PSCRAPER_HOST')
        token = os.getenv('PSCRAPER_TOKEN')
        super().__init__(f'https://{host}/api/v1', token)

    # ===== GET =====
    def seller_get(self, **kwargs):
        return self.get_request('/seller/', params=kwargs)

    def vehicle_get(self, marketplace, **kwargs):
        return self.get_request(MARKETPLACE_URLS[marketplace], params=kwargs)

    def history_get(self, **kwargs):
        return self.get_request('/history/', params=kwargs)

    # ===== POST =====
    def seller_post(self, **kwargs):
        return self.post_request('/seller/', data=kwargs)

    def vehicle_post(self, marketplace, **kwargs):
        return self.post_request(MARKETPLACE_URLS[marketplace], data=kwargs)

    def history_post(self, **kwargs):
        return self.post_request('/history/', data=kwargs)

    # ===== PATCH =====
    def seller_patch(self, phone_number, **kwargs):
        return self.patch_request(f'/seller/{phone_number}/', data=kwargs)

    def vehicle_patch(self, marketplace, vin, **kwargs):
        return self.patch_request(f'{MARKETPLACE_URLS[marketplace]}{vin}/', data=kwargs)
