import datetime

DATE_FORMAT = '%m-%d-%Y'
CURR_DATE = datetime.datetime.now().strftime(DATE_FORMAT)

CARS_COM_SEARCH_URL = 'https://www.cars.com/for-sale/searchresults.action/?fuelTypeId=38745&page={}&perPage={}&rd={}' \
                      '&zc={}&userSetIxt=true'
CARS_COM_VEHICLE_HREF_FORMAT = 'https://www.cars.com/vehicledetail/detail/{}/overview/'

GOOGLE_MAPS_REQUEST_URL = 'https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}'

DEALER_RATING_FORMAT = '({}) {} Reviews'
DEALER_ADDRESS_FORMAT = '{}, {}, {}'
LISTINGS_PER_PAGE = '100'

TOTAL_NUM_PAGES = 'totalNumPages'
LISTING_ID = 'listingId'
VIN = 'vin'
MAKE = 'make'
MODEL = 'model'
TRIM = 'trim'
BODY_STYLE = 'bodyStyle'
YEAR = 'year'
PRICE = 'price'
MILEAGE = 'mileage'
FIRST_DATE = 'firstDate'
LAST_DATE = 'lastDate'
DURATION = 'duration'
LISTING_HREF = 'listingHref'
DEALER_KEY = 'dealer'
DEALER_NAME = 'dealerName'
DEALER_PHONE_NUMBER = 'dealerPhoneNumber'
DEALER_ADDRESS = 'dealerAddress'
DEALER_RATING = 'dealerRating'

NOT_APPLICABLE = 'N/A'
NAME = 'name'
PHONE_NUMBER = 'phoneNumber'
STREET_ADDRESS = 'streetAddress'
CITY = 'city'
STATE = 'state'
RATING = 'rating'
REVIEW_COUNT = 'reviewCount'
SELLER = 'seller'
PAGE = 'page'
VEHICLE = 'vehicle'

SEARCH = 'search'
CAR_FORMATTING = """
Listing ID:         {}
VIN:                {}
Make:               {}
Model:              {}
Trim:               {}
Body Style:         {}
Price:              {}
Mileage:            {}
Year:               {}
First Date:         {}
Last Date:          {}
Duration:           {}
Href:               {}
Dealer Name:        {}
Dealer Phone:       {}
Dealer Address:     {}
Dealer Rating:      {}
"""
DEALER_FORMATTING = """
Name:         {}
Phone Number: {}
Rating:       {}
Location:     {}
"""

NUM_CARS_HEADER = 'Num of Cars'
AVG_DURATION_HEADER = 'Avg. Duration(days)'
AVG_PRICE_HEADER = 'Avg. Price($)'
DEALER_SHEET_NAME = 'Dealers'
MANUFACTURER_SHEET_NAME = 'Manufacturers'
MANUFACTURER_SHEET_INDEX = 0
DEALER_SHEET_INDEX = 1

LISTING_ID_COL = 0
VIN_COL = 1
MAKE_COL = 2
MODEL_COL = 3
TRIM_COL = 4
BODY_STYLE_COL = 5
FIRST_DATE_COL = 6
LAST_DATE_COL = 7
DURATION_COL = 8
PRICE_COL = 9
MILEAGE_COL = 10
YEAR_COL = 11
DEALER_NAME_COL = 12
DEALER_PHONE_COL = 13
DEALER_RATING_COL = 14
DEALER_ADDRESS_COL = 15
HREF_COL = 16

DEFAULT_ROW_WIDTH = 20
LISTING_ID_COL_WIDTH = DEFAULT_ROW_WIDTH
VIN_COL_WIDTH = 25
MAKE_COL_WIDTH = 15
MODEL_COL_WIDTH = 25
DEALER_NAME_COL_WIDTH = 25
DEALER_PHONE_COL_WIDTH = 15
DEALER_RATING_COL_WIDTH = DEFAULT_ROW_WIDTH
DEALER_ADDRESS_COL_WIDTH = 30
HREF_COL_WIDTH = 60

LISTING_ID_HEADER = 'Listing ID'
VIN_HEADER = 'VIN'
MAKE_HEADER = 'Make'
MODEL_HEADER = 'Model'
TRIM_HEADER = 'Trim'
BODY_STYLE_HEADER = 'Body Style'
FIRST_DATE_HEADER = 'Date First Available'
LAST_DATE_HEADER = 'Date Last Available'
DURATION_HEADER = 'Duration'
PRICE_HEADER = 'Price'
MILEAGE_HEADER = 'Mileage'
YEAR_HEADER = 'Year'
DEALER_NAME_HEADER = 'Dealer Name'
DEALER_PHONE_HEADER = 'Dealer Phone'
DEALER_RATING_HEADER = 'Dealer Rating'
DEALER_ADDRESS_HEADER = 'Dealer Address'
HREF_HEADER = 'Href'

CELL_FORMAT_1 = {
    'bg_color': '#FFC7CE',
    'font_color': '#9C0006'
}
CELL_FORMAT_2 = {
    'bg_color': '#C6EFCE',
    'font_color': '#006100'
}
MASTER_TABLE_HEADER_FORMAT = {
    'border': 1,
    'bg_color': '#C6EFCE',
    'bold': True,
    'text_wrap': True,
    'align': 'center',
    'indent': 1,
}
MANUF_SHEET_COND_FORMAT_1 = {
    'type': '3_color_scale',
    'criteria': '<',
    'value': 20,
    'format': 'PLACEHOLDER'
}
MANUF_SHEET_COND_FORMAT_2 = {
    'type': '3_color_scale',
    'criteria': '>=',
    'value': 20,
    'format': 'PLACEHOLDER'
}
SOLD_CAR_COL = '#97f9c8'
AVAIL_CAR_COL = '#bde0ff'
BG_COL_KEY = 'bg_color'
MT_CELL_FORMAT = {
    BG_COL_KEY: 'PLACEHOLDER',
    'text_wrap': True,
}
DEALER_SHEET_COND_FORMAT_1 = {
    'type': '3_color_scale',
    'criteria': '<',
    'value': 35,
    'format': 'PLACEHOLDER'
}
DEALER_SHEET_COND_FORMAT_2 = {
    'type': '3_color_scale',
    'criteria': '>=',
    'value': 35,
    'format': 'PLACEHOLDER'
}

TRIM_COL_WIDTH = BODY_STYLE_COL_WIDTH = 15
FIRST_DATE_COL_WIDTH = LAST_DATE_COL_WIDTH = DEFAULT_ROW_WIDTH
DURATION_COL_WIDTH = PRICE_COL_WIDTH = MILEAGE_COL_WIDTH = YEAR_COL_WIDTH = 10
