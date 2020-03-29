from pscraper.utils.base_api import BaseAPI


class API(BaseAPI):
    def __init__(self, username, password, localhost=False):
        url = 'http://pscraper.herokuapp.com/pscraper/' if not localhost else 'http://localhost:8000/pscraper/'
        super().__init__(url, (username, password))

    # ===== GET =====
    def seller_get(self, **kwargs):
        return self.get_request('seller/', data=kwargs)

    def vehicle_get(self, **kwargs):
        return self.get_request('vehicle/', data=kwargs)

    # ===== POST =====
    def seller_post(self, **kwargs):
        return self.post_request('seller/', data=kwargs)

    def vehicle_post(self, **kwargs):
        return self.post_request('vehicle/', data=kwargs)

    # ===== PATCH =====
    def seller_patch(self, **kwargs):
        return self.patch_request('seller/', data=kwargs)

    def vehicle_patch(self, **kwargs):
        return self.patch_request('vehicle/', data=kwargs)
