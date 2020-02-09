from pscraper._consts import NAME, RATING, SELLER_FMT, PHONE_NUMBER, ADDRESS, DEALER_ADDRESS_FORMAT, STATE, \
    CITY, STREET_ADDRESS


class Seller:
    def __init__(self, seller):
        """
        Args:
            seller (dict): Dictionary containing seller information

        Attributes:
            name (str): Seller name
            phone_number (str): Seller phone number
            rating (str): Seller rating and number of ratings
            address (str): Seller address

        """
        self.name = seller[NAME]
        self.phone_number = seller[PHONE_NUMBER]
        self.rating = seller[RATING]
        try:
            self.address = seller[ADDRESS]
        except KeyError:
            self.address = DEALER_ADDRESS_FORMAT.format(seller[STREET_ADDRESS], seller[CITY], seller[STATE])

    def __repr__(self):
        return SELLER_FMT.format(self.name, self.phone_number, self.rating, self.address)

    @property
    def json(self):
        return {
            NAME: self.name,
            PHONE_NUMBER: self.phone_number,
            RATING: self.rating,
            ADDRESS: self.address,
        }
