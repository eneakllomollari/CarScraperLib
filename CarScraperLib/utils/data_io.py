import csv
import datetime
import logging

import xlrd
import xlsxwriter

from ..classes.dealer import Dealer
from ..classes.vehicle import Vehicle
from ..constants.consts import DATE_FORMAT, MASTER_TABLE_HEADER_FORMAT, SOLD_CAR_COL, AVAIL_CAR_COL, \
    BG_COL_KEY, MT_CELL_FORMAT, LISTING_ID_COL, VIN_COL, MAKE_COL, MODEL_COL, TRIM_COL, BODY_STYLE_COL, \
    FIRST_DATE_COL, LAST_DATE_COL, DURATION_COL, PRICE_COL, MILEAGE_COL, YEAR_COL, DEALER_NAME_COL, DEALER_PHONE_COL, \
    DEALER_RATING_COL, DEALER_ADDRESS_COL, HREF_COL, LISTING_ID_COL_WIDTH, VIN_COL_WIDTH, MAKE_COL_WIDTH, \
    MODEL_COL_WIDTH, DEALER_NAME_COL_WIDTH, DEALER_PHONE_COL_WIDTH, DEALER_RATING_COL_WIDTH, DEALER_ADDRESS_COL_WIDTH, \
    HREF_COL_WIDTH, LISTING_ID_HEADER, VIN_HEADER, MAKE_HEADER, MODEL_HEADER, TRIM_HEADER, BODY_STYLE_HEADER, \
    FIRST_DATE_HEADER, LAST_DATE_HEADER, DURATION_HEADER, PRICE_HEADER, MILEAGE_HEADER, YEAR_HEADER, \
    DEALER_NAME_HEADER, DEALER_PHONE_HEADER, DEALER_RATING_HEADER, DEALER_ADDRESS_HEADER, HREF_HEADER, TRIM_COL_WIDTH, \
    BODY_STYLE_COL_WIDTH, FIRST_DATE_COL_WIDTH, LAST_DATE_COL_WIDTH, DURATION_COL_WIDTH, PRICE_COL_WIDTH, \
    MILEAGE_COL_WIDTH, YEAR_COL_WIDTH

logger = logging.getLogger(__name__)


def get_master_table(master_table_loc, jsonify=False):
    """
    :param master_table_loc:  path of the master table excel file
    :param jsonify: if True returns a `dict` representation of all the vehicle data,
                    else    returns a `dict` with 'listing_id' as keys and `classes.Vehicle` as values
    :return: `classes.Vehicle` or `dict` representation of the cars in `master_table_loc`
    """
    master_table = {}
    sheet = xlrd.open_workbook(master_table_loc).sheet_by_index(0)
    for i in range(sheet.nrows):
        if i == 0:
            continue
        get = sheet.cell_value
        my_car = Vehicle(
            listing_id=get(i, LISTING_ID_COL),
            vin=get(i, VIN_COL),
            make=get(i, MAKE_COL),
            model=get(i, MODEL_COL),
            trim=get(i, TRIM_COL),
            body_style=get(i, BODY_STYLE_COL),
            first_date=get(i, FIRST_DATE_COL),
            last_date=get(i, LAST_DATE_COL),
            duration=_get_duration(get(i, FIRST_DATE_COL), get(i, LAST_DATE_COL)),
            price=get(i, PRICE_COL),
            mileage=get(i, MILEAGE_COL),
            year=get(i, YEAR_COL),
            href=get(i, HREF_COL),
            dealer=Dealer(
                name=get(i, DEALER_NAME_COL),
                phone_number=get(i, DEALER_PHONE_COL),
                rating=get(i, DEALER_RATING_COL),
                address=get(i, DEALER_ADDRESS_COL),
            ),
        )
        master_table[my_car.listing_id] = my_car if not jsonify else my_car.json
    return master_table


def save_master_table(master_table_loc, master_table):
    """
    :param master_table_loc: path where the master table excel file will be saved
    :param master_table: `dict` object with `listing_id` keys and `classes.Car` objects
    :return: None
    """
    column = 0
    row = 1
    workbook = xlsxwriter.Workbook(master_table_loc)
    worksheet = workbook.add_worksheet()
    header_format = workbook.add_format(MASTER_TABLE_HEADER_FORMAT)

    _save_column_widths(worksheet)
    _save_worksheet_headers(worksheet, column, header_format)

    for car in master_table.values():
        _save_car_to_worksheet(worksheet, row, column, car, workbook)
        row += 1
    workbook.close()
    logger.info(f'\t Saved master table data to {master_table_loc}')


def get_history(path):
    """
    :param path: path of the csv file that contains the changes over time
        required file format:
            unique_identifier_1,date1,value1,date2,value2
            unique_identifier_2,date21,value21
    :return: `dict` with `unique_identifier` as key and `list` with the history as value
    """
    history_dict = {}
    with open(path, 'r') as csv_file:
        for row in csv.reader(csv_file, delimiter=','):
            val = {}
            history_row = row[1:]
            for i in range(len(history_row)):
                val[history_row[i + 1]] = history_row[i]
                i += 2
            history_dict[row[0]] = val
    return history_dict


def _save_car_to_worksheet(worksheet, row, column, car, workbook):
    curr_date = datetime.datetime.now().strftime(DATE_FORMAT)
    MT_CELL_FORMAT[BG_COL_KEY] = SOLD_CAR_COL if car.last_date != curr_date else AVAIL_CAR_COL

    cell_format = workbook.add_format(MT_CELL_FORMAT)

    worksheet.write(row, column + LISTING_ID_COL, car.listing_id, cell_format)
    worksheet.write(row, column + VIN_COL, car.vin, cell_format)
    worksheet.write(row, column + MAKE_COL, car.make, cell_format)
    worksheet.write(row, column + MODEL_COL, car.model, cell_format)
    worksheet.write(row, column + TRIM_COL, car.trim, cell_format)
    worksheet.write(row, column + BODY_STYLE_COL, car.body_style, cell_format)
    worksheet.write(row, column + FIRST_DATE_COL, car.first_date, cell_format)
    worksheet.write(row, column + LAST_DATE_COL, car.last_date, cell_format)
    worksheet.write(row, column + DURATION_COL, car.duration, cell_format)
    worksheet.write(row, column + PRICE_COL, car.price)
    worksheet.write(row, column + MILEAGE_COL, car.mileage)
    worksheet.write(row, column + YEAR_COL, car.year)
    worksheet.write(row, column + DEALER_NAME_COL, car.dealer.name)
    worksheet.write(row, column + DEALER_PHONE_COL, car.dealer.phone_number)
    worksheet.write(row, column + DEALER_RATING_COL, car.dealer.rating)
    worksheet.write(row, column + DEALER_ADDRESS_COL, car.dealer.address)
    worksheet.write(row, column + HREF_COL, car.href)


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
    worksheet.write(0, col + DEALER_NAME_COL, DEALER_NAME_HEADER, header_format)
    worksheet.write(0, col + DEALER_PHONE_COL, DEALER_PHONE_HEADER, header_format)
    worksheet.write(0, col + DEALER_RATING_COL, DEALER_RATING_HEADER, header_format)
    worksheet.write(0, col + DEALER_ADDRESS_COL, DEALER_ADDRESS_HEADER, header_format)
    worksheet.write(0, col + 16, HREF_HEADER, header_format)


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
    worksheet.set_column(DEALER_NAME_COL, DEALER_NAME_COL, DEALER_NAME_COL_WIDTH)
    worksheet.set_column(DEALER_PHONE_COL, DEALER_PHONE_COL, DEALER_PHONE_COL_WIDTH)
    worksheet.set_column(DEALER_RATING_COL, DEALER_RATING_COL, DEALER_RATING_COL_WIDTH)
    worksheet.set_column(DEALER_ADDRESS_COL, DEALER_ADDRESS_COL, DEALER_ADDRESS_COL_WIDTH)
    worksheet.set_column(HREF_COL, HREF_COL, HREF_COL_WIDTH)


def _get_duration(first_date, last_date):
    return (datetime.datetime.strptime(last_date, DATE_FORMAT) - datetime.datetime.strptime(first_date,
                                                                                            DATE_FORMAT)).days
