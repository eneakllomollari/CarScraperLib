from consts import DEALER_NAME, DEALER_PHONE_NUMBER, DEALER_ADDRESS, DEALER_RATING, DEALER_FORMATTING


class Dealer:
    def __init__(self, name=None, phone_number=None, rating=None, address=None):
        self.name = name
        self.phone_number = phone_number
        self.rating = rating
        self.address = address

    def __repr__(self):
        return DEALER_FORMATTING.format(
            self.name,
            self.phone_number,
            self.rating,
            self.address
        )

    @property
    def json(self):
        return {
            DEALER_NAME: self.name,
            DEALER_PHONE_NUMBER: self.phone_number,
            DEALER_RATING: self.rating,
            DEALER_ADDRESS: self.address
        }
