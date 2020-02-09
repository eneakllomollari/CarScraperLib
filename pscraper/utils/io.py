import datetime

import xlrd
import xlsxwriter

from ..classes.vehicle import Vehicle
from .._consts import DATE_FORMAT, MASTER_TABLE_HEADER_FORMAT, SOLD_CAR_COL, AVAIL_CAR_COL, BG_COL_KEY, \
    MT_CELL_FORMAT, LISTING_ID_COL, VIN_COL, MAKE_COL, MODEL_COL, YEAR_COL, TRIM_COL, MILEAGE_COL, \
    PRICE_COL, BODY_STYLE_COL, FIRST_DATE_COL, LAST_DATE_COL, DURATION_COL, NAME_COL, MODEL_HEADER, \
    PHONE_COL, RATING_COL, LISTING_ID_COL_WIDTH, VIN_COL_WIDTH, MAKE_COL_WIDTH, TRIM_HEADER, ADDRESS_COL, \
    MODEL_COL_WIDTH, LISTING_ID_HEADER, VIN_HEADER, MAKE_HEADER, BODY_STYLE_HEADER, FIRST_DATE_HEADER, \
    LAST_DATE_HEADER, DURATION_HEADER, PRICE_HEADER, MILEAGE_HEADER, YEAR_HEADER, DEALER_NAME_HEADER, \
    DEALER_PHONE_HEADER, MILEAGE_COL_WIDTH, TRIM_COL_WIDTH, BODY_STYLE_COL_WIDTH, YEAR_COL_WIDTH, \
    FIRST_DATE_COL_WIDTH, LAST_DATE_COL_WIDTH, DURATION_COL_WIDTH, PRICE_COL_WIDTH, LISTING_ID, VIN, MAKE, \
    MODEL, TRIM, NAME, BODY_STYLE, PRICE, MILEAGE, YEAR, SELLER, FIRST_DATE, LAST_DATE, DURATION, \
    PHONE_NUMBER, RATING, ADDRESS, DEALER_RATING_HEADER, DEALER_ADDRESS_HEADER


def get_master_table(mastertable_path, jsonify=False):
    """Builds a dictionary by reading `mastertable_path`

    Args:
        mastertable_path (str): Path of the master table excel file
        jsonify (bool): Conditions the format of the return data. If `True` returns a dictionary
        representation of all the vehicle data, otherwise returns a dictionary with `listingID`s as keys and
        `Vehicle`s as values

    Returns:
        dict: `listingID` as keys and values of `Vehicle`s or a dictionary representation of the vehicles

    """
    master_table = {}
    sheet = xlrd.open_workbook(mastertable_path).sheet_by_index(0)
    for i in range(sheet.nrows):
        if i == 0:
            continue
        vehicle = Vehicle({
            LISTING_ID: sheet.cell_value(i, LISTING_ID_COL),
            VIN: sheet.cell_value(i, VIN_COL),
            MAKE: sheet.cell_value(i, MAKE_COL),
            MODEL: sheet.cell_value(i, MODEL_COL),
            TRIM: sheet.cell_value(i, TRIM_COL),
            BODY_STYLE: sheet.cell_value(i, BODY_STYLE_COL),
            PRICE: sheet.cell_value(i, PRICE_COL),
            MILEAGE: sheet.cell_value(i, MILEAGE_COL),
            YEAR: sheet.cell_value(i, YEAR_COL),
            FIRST_DATE: sheet.cell_value(i, FIRST_DATE_COL),
            LAST_DATE: sheet.cell_value(i, LAST_DATE_COL),
            DURATION: sheet.cell_value(i, DURATION_COL),
            SELLER: {
                NAME: sheet.cell_value(i, NAME_COL),
                PHONE_NUMBER: sheet.cell_value(i, PHONE_COL),
                RATING: sheet.cell_value(i, RATING_COL),
                ADDRESS: sheet.cell_value(i, ADDRESS_COL),
            },
        })
        master_table[vehicle.listing_id] = vehicle if not jsonify else vehicle.json
    return master_table


def save_master_table(mastertable, mastertable_path):
    """Saves `master_table` to `master_table_loc`

    Args:
        mastertable_path (str): path where the master table excel file will be saved
        mastertable (dict): dictionary with `listingID` keys and `Vehicle` values

    """
    column = 0
    workbook = xlsxwriter.Workbook(mastertable_path)
    worksheet = workbook.add_worksheet()
    header_format = workbook.add_format(MASTER_TABLE_HEADER_FORMAT)

    _save_column_widths(worksheet)
    _save_worksheet_headers(worksheet, column, header_format)

    for row, car in enumerate(mastertable.values(), start=1):
        _save_car_to_worksheet(worksheet, row, column, car, workbook)
    workbook.close()


def _save_car_to_worksheet(worksheet, row, col, car, workbook):
    curr_date = datetime.datetime.now().strftime(DATE_FORMAT)
    MT_CELL_FORMAT[BG_COL_KEY] = SOLD_CAR_COL if car.last_date != curr_date else AVAIL_CAR_COL
    cell_format = workbook.add_format(MT_CELL_FORMAT)
    worksheet.write(row, col + LISTING_ID_COL, car.listing_id, cell_format)
    worksheet.write(row, col + VIN_COL, car.vin, cell_format)
    worksheet.write(row, col + MAKE_COL, car.make, cell_format)
    worksheet.write(row, col + MODEL_COL, car.model, cell_format)
    worksheet.write(row, col + TRIM_COL, car.trim, cell_format)
    worksheet.write(row, col + BODY_STYLE_COL, car.body_style, cell_format)
    worksheet.write(row, col + FIRST_DATE_COL, car.first_date, cell_format)
    worksheet.write(row, col + LAST_DATE_COL, car.last_date, cell_format)
    worksheet.write(row, col + DURATION_COL, car.duration, cell_format)
    worksheet.write(row, col + PRICE_COL, car.price)
    worksheet.write(row, col + MILEAGE_COL, car.mileage)
    worksheet.write(row, col + YEAR_COL, car.year)
    worksheet.write(row, col + NAME_COL, car.seller.name)
    worksheet.write(row, col + PHONE_COL, car.seller.phone_number)
    worksheet.write(row, col + RATING_COL, car.seller.rating)
    worksheet.write(row, col + ADDRESS_COL, car.seller.address)


def _save_worksheet_headers(worksheet, col, header_format):
    worksheet.write(0, col + LISTING_ID_COL, LISTING_ID_HEADER, header_format)
    worksheet.write(0, col + VIN_COL, VIN_HEADER, header_format)
    worksheet.write(0, col + MAKE_COL, MAKE_HEADER, header_format)
    worksheet.write(0, col + MODEL_COL, MODEL_HEADER, header_format)
    worksheet.write(0, col + TRIM_COL, TRIM_HEADER, header_format)
    worksheet.write(0, col + BODY_STYLE_COL, BODY_STYLE_HEADER, header_format)
    worksheet.write(0, col + FIRST_DATE_COL, FIRST_DATE_HEADER, header_format)
    worksheet.write(0, col + LAST_DATE_COL, LAST_DATE_HEADER, header_format)
    worksheet.write(0, col + DURATION_COL, DURATION_HEADER, header_format)
    worksheet.write(0, col + PRICE_COL, PRICE_HEADER, header_format)
    worksheet.write(0, col + MILEAGE_COL, MILEAGE_HEADER, header_format)
    worksheet.write(0, col + YEAR_COL, YEAR_HEADER, header_format)
    worksheet.write(0, col + NAME_COL, DEALER_NAME_HEADER, header_format)
    worksheet.write(0, col + PHONE_COL, DEALER_PHONE_HEADER, header_format)
    worksheet.write(0, col + RATING_COL, DEALER_RATING_HEADER, header_format)
    worksheet.write(0, col + ADDRESS_COL, DEALER_ADDRESS_HEADER, header_format)


def _save_column_widths(worksheet):
    worksheet.set_column(LISTING_ID_COL, LISTING_ID_COL, LISTING_ID_COL_WIDTH)
    worksheet.set_column(VIN_COL, VIN_COL, VIN_COL_WIDTH)
    worksheet.set_column(MAKE_COL, MAKE_COL, MAKE_COL_WIDTH)
    worksheet.set_column(MODEL_COL, MODEL_COL, MODEL_COL_WIDTH)
    worksheet.set_column(TRIM_COL, TRIM_COL, TRIM_COL_WIDTH)
    worksheet.set_column(BODY_STYLE_COL, BODY_STYLE_COL, BODY_STYLE_COL_WIDTH)
    worksheet.set_column(FIRST_DATE_COL, FIRST_DATE_COL, FIRST_DATE_COL_WIDTH)
    worksheet.set_column(LAST_DATE_COL, LAST_DATE_COL, LAST_DATE_COL_WIDTH)
    worksheet.set_column(DURATION_COL, DURATION_COL, DURATION_COL_WIDTH)
    worksheet.set_column(PRICE_COL, PRICE_COL, PRICE_COL_WIDTH)
    worksheet.set_column(MILEAGE_COL, MILEAGE_COL, MILEAGE_COL_WIDTH)
    worksheet.set_column(YEAR_COL, YEAR_COL, YEAR_COL_WIDTH)
