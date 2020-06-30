from datetime import datetime

DATE_FMT = '%Y-%m-%d'
CURR_DATE = datetime.now().strftime(DATE_FMT)
CARS_COM_QUERY = 'https://www.cars.com/for-sale/searchresults.action/?dealerType=localOnly&fuelTypeId=38745&page={}' \
                 '&perPage=100&rd=99999&zc=95616&userSetIxt=true'
AUTOTRADER_QUERY = 'https://www.autotrader.com/cars-for-sale/Electric?fuelTypeGroup=ELE&numRecords=100&searchRadius=0' \
                   '&zip=95616&firstRecord={}'
AUTOTRADER_OWNER_QUERY = 'https://www.autotrader.com/car-dealers/'
CARS_TOKEN = 'CARS.digitalData = '
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/80.0.3987.149 Safari/537.36'
}
MAX_THREADS = 25
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
LAT = 'lat'
LNG = 'lng'
DURATION = 'duration'
PHONE_NUMBER = 'phoneNumber'
STREET_ADDRESS = 'streetAddress'
CITY = 'city'
LISTING_ID = 'listingId'
STATE = 'state'
VIN = 'vin'
SELLER = 'seller'
VEHICLE = 'vehicle'
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
OWNER = 'owner'
