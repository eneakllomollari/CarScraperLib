from datetime import datetime

DATE_FMT = '%Y-%m-%d'
CURR_DATE = datetime.now().strftime(DATE_FMT)
CARS_COM_QUERY = 'https://www.cars.com/for-sale/searchresults.action/?dealerType=localOnly&fuelTypeId=38745&' \
                 'page={}&perPage=100&rd={}&zc={}&userSetIxt=true'
AUTOTRADER_QUERY = 'https://www.autotrader.com/cars-for-sale/Electric?fuelTypeGroup=ELE&numRecords=100&' \
                   'searchRadius={}&zip={}&firstRecord={}'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/80.0.3987.149 Safari/537.36'
}
ALLOWED_CARS_RD = [10, 20, 30, 40, 50, 75, 100, 150, 200, 250, 500, 99999]
ALLOWED_AT_RD = [0, 10, 25, 50, 75, 100, 200, 300, 400, 500]
ALLOWED_RD = set(ALLOWED_CARS_RD).intersection(ALLOWED_AT_RD)

ADDRESS_FORMAT = '{}, {}, {}'
MAKE = 'make'
MODEL = 'model'
TRIM = 'trim'
BODY_STYLE = 'bodyStyle'
YEAR = 'year'
PRICE = 'price'
MILEAGE = 'mileage'
FIRST_DATE = 'firstDate'
LAST_DATE = 'lastDate'
SELLER_ID = 'sellerID'
NAME = 'name'
DURATION = 'duration'
PHONE_NUMBER = 'phoneNumber'
STREET_ADDRESS = 'streetAddress'
CITY = 'city'
LISTING_ID = 'listingId'
STATE = 'state'
VIN = 'vin'
SELLER = 'seller'
VEHICLE = 'vehicle'
STATES = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY',
          'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH',
          'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']
PAGE = 'page'
SEARCH = 'search'
TOTAL_NUM_PAGES = 'totalNumPages'
INITIAL_STATE = 'initialState'
DOMAIN = 'domain'
SRP = 'srp'
RESULTS = 'results'
COUNT = 'count'
INVENTORY = 'inventory'
ZIP_CODE = 'zip'
OWNER_NAME = 'ownerName'
