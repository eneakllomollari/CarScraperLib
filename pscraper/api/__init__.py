from pscraper.utils.base_api import BaseAPI


class PscraperAPI(BaseAPI):
    """
    Provides the APIs to interact with the pscraper backend application
    """

    def __init__(self, token, host):
        super().__init__(f'https://{host}/api/v1/', token)

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
