from pscraper.utils.base_api import BaseAPI


class API(BaseAPI):
    def __init__(self, username, password):
        super().__init__(f'http://pscraper.herokuapp.com/pscraper/', (username, password))

    # ===== GET =====
    def seller_get(self, **kwargs):
        return self.get_request('seller/', params=kwargs)

    def vehicle_get(self, **kwargs):
        return self.get_request('vehicle/', params=kwargs)

    # ===== PUT =====
    def seller_put(self, seller):
        return self.put_request('seller/', data=seller)

    def vehicle_put(self, vehicle):
        return self.put_request('vehicle/', data=vehicle)

    # ===== PATCH =====
    def seller_patch(self, primary_key, **kwargs):
        return self.patch_request('seller/', params={'id': primary_key}, data=kwargs)

    def vehicle_patch(self, primary_key, **kwargs):
        return self.patch_request('vehicle/', params={'id': primary_key}, data=kwargs)
