from pscraper.utils.base_api import BaseAPI


class API(BaseAPI):
    """
    Provides the APIs to interact with the database
    """

    def __init__(self, username, password, localhost=False):
        host = 'http://pscraper.herokuapp.com/' if not localhost else 'http://localhost:8000/'
        super().__init__(f'{host}api/v1/', (username, password))

    # ===== GET =====
    def seller_get(self, **kwargs):
        return self.get_request('seller/', params=kwargs)

    def vehicle_get(self, **kwargs):
        return self.get_request('vehicle/', params=kwargs)

    def history_get(self, **kwargs):
        return self.get_request('history/', params=kwargs)

    # ===== POST =====
    def seller_post(self, **kwargs):
        return self.post_request('seller/', data=kwargs)

    def vehicle_post(self, **kwargs):
        return self.post_request('vehicle/', data=kwargs)

    def history_post(self, **kwargs):
        return self.post_request('history/', data=kwargs)

    # ===== PATCH =====
    def seller_patch(self, phone_number, **kwargs):
        return self.patch_request(f'seller/{phone_number}/', data=kwargs)

    def vehicle_patch(self, vin, **kwargs):
        return self.patch_request(f'vehicle/{vin}/', data=kwargs)
