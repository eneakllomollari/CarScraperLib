from ..constants.consts import VIN, MAKE, MODEL, TRIM, BODY_STYLE, YEAR, PRICE, MILEAGE, FIRST_DATE, LAST_DATE, \
    DURATION, LISTING_HREF, DEALER_KEY, CAR_FORMATTING, LISTING_ID


class Vehicle:
    def __init__(self, listing_id, vin, make=None, model=None, trim=None, body_style=None, price=None,
                 mileage=None, year=None, first_date=None, last_date=None, duration=None, href=None, dealer=None):
        self.listing_id = listing_id
        self.vin = vin
        self.make = make
        self.model = model
        self.trim = trim
        self.body_style = body_style
        self.price = price
        self.mileage = mileage
        self.year = year
        self.first_date = first_date
        self.last_date = last_date
        self.duration = duration
        self.href = href
        self.dealer = dealer

    def __repr__(self):
        return CAR_FORMATTING.format(
            self.listing_id,
            self.vin,
            self.make,
            self.model,
            self.trim,
            self.body_style,
            self.price,
            self.mileage,
            self.year,
            self.first_date,
            self.last_date,
            self.duration,
            self.href,
            self.dealer.name,
            self.dealer.phone_number,
            self.dealer.address,
            self.dealer.rating
        )

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
            LISTING_HREF: self.href,
            DEALER_KEY: self.dealer.json
        }
