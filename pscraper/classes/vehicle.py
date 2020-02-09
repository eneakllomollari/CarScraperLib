from pscraper._consts import VIN, MAKE, MODEL, TRIM, BODY_STYLE, YEAR, PRICE, MILEAGE, FIRST_DATE, \
    LAST_DATE, DURATION, VEHICLE_FMT, LISTING_ID, SELLER, NOT_APPLICABLE
from .seller import Seller


class Vehicle:
    def __init__(self, vehicle):
        """
        Args:
            vehicle: Dictionary containing vehicle information

        Attributes:
            listing_id (str): Unique listing ID given to the vehicle by the publisher(cars.com)
            vin (str): Vehicle Identification Number
            make (str): Vehicle make
            model (str): Vehicle model
            trim (str): Vehicle trim
            body_style (str): Vehicle body style
            mileage (str): Vehicle mileage
            year (str): Vehicle year
            seller (Seller): Vehicle seller
            first_date (str): The first date the vehicle was available for purchase
            last_date (str): The last date the vehicle was available for purchase
            duration (int): The duration in days the vehicle was available for

        """
        self.listing_id = vehicle[LISTING_ID]
        self.vin = vehicle[VIN]
        self.make = vehicle[MAKE]
        self.model = vehicle[MODEL]
        self.trim = vehicle[TRIM]
        self.body_style = vehicle[BODY_STYLE]
        self.price = vehicle[PRICE]
        self.mileage = vehicle[MILEAGE]
        self.year = vehicle[YEAR]
        self.seller = Seller(vehicle[SELLER])
        self.first_date = NOT_APPLICABLE if FIRST_DATE not in vehicle else vehicle[FIRST_DATE]
        self.last_date = NOT_APPLICABLE if LAST_DATE not in vehicle else vehicle[LAST_DATE]
        self.duration = NOT_APPLICABLE if DURATION not in vehicle else vehicle[DURATION]

    def __repr__(self):
        return VEHICLE_FMT.format(self.listing_id, self.vin, self.make, self.model, self.trim,
                                  self.body_style, self.price, self.mileage, self.year, self.first_date,
                                  self.last_date, self.duration, self.seller.name, self.seller.phone_number,
                                  self.seller.address, self.seller.rating)

    @property
    def json(self):
        return {
            LISTING_ID: self.listing_id,
            VIN: self.vin,
            MAKE: self.make,
            MODEL: self.model,
            TRIM: self.trim,
            BODY_STYLE: self.body_style,
            YEAR: self.year,
            PRICE: self.price,
            MILEAGE: self.mileage,
            FIRST_DATE: self.first_date,
            LAST_DATE: self.last_date,
            DURATION: self.duration,
            SELLER: self.seller.json
        }
