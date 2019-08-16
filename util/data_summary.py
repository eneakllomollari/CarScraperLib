import logging

import pandas as pd
import xlrd

from consts import MASTER_TABLE, SUMMARY_SOLD, SUMMARY_ALL, CURR_DATE, DATE_FORMAT, \
    CELL_FORMAT_1, CELL_FORMAT_2, MANUF_SHEET_COND_FORMAT_1, MANUF_SHEET_COND_FORMAT_2, NUM_CARS_HEADER, \
    AVG_DURATION_HEADER, AVG_PRICE_HEADER, DEALER_SHEET_NAME, MANUFACTURER_SHEET_NAME, MAKE_COL, LAST_DATE_COL, \
    DURATION_COL, PRICE_COL, DEALER_SHEET_COND_FORMAT_1, DEALER_SHEET_COND_FORMAT_2, DEFAULT_ROW_WIDTH, DEALER_NAME_COL

logger = logging.getLogger(__name__)


def main():
    writer_all = pd.ExcelWriter(SUMMARY_ALL, engine='xlsxwriter')
    writer_sold = pd.ExcelWriter(SUMMARY_SOLD, engine='xlsxwriter')

    dealer_main_all(writer_all)
    manuf_main_all(writer_all)
    writer_all.save()

    logger.info(f'Summarized dealer and manufacturer data for all cars in:    {SUMMARY_ALL}')

    dealer_main_sold(writer_sold)
    manuf_main_sold(writer_sold)
    writer_sold.save()

    logger.info(f'Summarized dealer and manufacturer data for sold cars only: {SUMMARY_SOLD}')


def dealer_main_sold(writer):
    dealer_dict = get_dict_dealers_sold()
    dealer_df = pd.DataFrame(dealer_dict, index=[NUM_CARS_HEADER, AVG_DURATION_HEADER]).transpose()

    dealer_df.to_excel(writer, sheet_name=DEALER_SHEET_NAME)

    workbook = writer.book
    worksheet = writer.sheets[DEALER_SHEET_NAME]

    dealer_cell_format(workbook, worksheet, len(dealer_dict) + 1)


def dealer_main_all(writer):
    dealer_dict = get_dict_dealers_all()
    dealer_df = pd.DataFrame(dealer_dict, index=[NUM_CARS_HEADER, AVG_DURATION_HEADER]).transpose()
    dealer_df.to_excel(writer, sheet_name=DEALER_SHEET_NAME)

    workbook = writer.book
    worksheet = writer.sheets[DEALER_SHEET_NAME]

    dealer_cell_format(workbook, worksheet, len(dealer_dict) + 1)


def manuf_main_all(writer):
    my_dict = get_dict_manufacturers_all()

    data_frame = pd.DataFrame(my_dict, index=[NUM_CARS_HEADER, AVG_PRICE_HEADER, AVG_DURATION_HEADER]).transpose()

    data_frame.to_excel(writer, sheet_name=MANUFACTURER_SHEET_NAME)

    workbook = writer.book
    worksheet = writer.sheets[MANUFACTURER_SHEET_NAME]

    manufacturer_cell_format(workbook, worksheet, len(my_dict) + 1)


def manuf_main_sold(writer):
    my_dict = get_dict_manufacturers_sold()

    index = [NUM_CARS_HEADER, AVG_PRICE_HEADER, AVG_DURATION_HEADER]
    data_frame = pd.DataFrame(my_dict, index=index).transpose()

    data_frame.to_excel(writer, sheet_name=MANUFACTURER_SHEET_NAME)

    workbook = writer.book
    worksheet = writer.sheets[MANUFACTURER_SHEET_NAME]

    manufacturer_cell_format(workbook, worksheet, len(my_dict) + 1)


def get_dict_dealers_all():
    dealer_dict = {}
    sheet = xlrd.open_workbook(MASTER_TABLE).sheet_by_index(0)

    for i in range(sheet.nrows):
        if i == 0:
            continue
        dealer_name = sheet.cell_value(i, DEALER_NAME_COL)
        duration = sheet.cell_value(i, DURATION_COL)
        if dealer_name not in dealer_dict.keys():
            dealer_dict[dealer_name] = [1, duration]
        else:
            dealer_dict[dealer_name][0] = dealer_dict[dealer_name][0] + 1
            dealer_dict[dealer_name][1] += duration

    for my_list in dealer_dict.values():
        my_list[1] = round(my_list[1] / my_list[0], 2)

    return dealer_dict


def get_dict_dealers_sold():
    dealer_dict = {}
    sheet = xlrd.open_workbook(MASTER_TABLE).sheet_by_index(0)

    for i in range(sheet.nrows):
        if i == 0:
            continue
        dealer_name = sheet.cell_value(i, DEALER_NAME_COL)
        last_date = sheet.cell_value(i, LAST_DATE_COL)
        duration = int(sheet.cell_value(i, DURATION_COL))

        if CURR_DATE().strftime(DATE_FORMAT) == last_date:
            continue
        elif dealer_name not in dealer_dict.keys():
            dealer_dict[dealer_name] = [1, duration]
        else:
            dealer_dict[dealer_name][0] = dealer_dict[dealer_name][0] + 1
            dealer_dict[dealer_name][1] += duration

    for my_list in dealer_dict.values():
        my_list[1] = round(my_list[1] / my_list[0], 2)

    return dealer_dict


def get_dict_manufacturers_all():
    manufacturer_dict = {}
    sheet = xlrd.open_workbook(MASTER_TABLE).sheet_by_index(0)

    for i in range(sheet.nrows):
        if i == 0:
            continue

        make = sheet.cell_value(i, MAKE_COL)
        duration = int(sheet.cell_value(i, DURATION_COL))
        price = sheet.cell_value(i, PRICE_COL)

        if not price or price == 'N/A':
            continue

        if make not in manufacturer_dict.keys():
            manufacturer_dict[make] = [1, float(price), duration]
        else:
            manufacturer_dict[make][0] += 1
            manufacturer_dict[make][1] += float(price)
            manufacturer_dict[make][2] += duration

    for my_list in manufacturer_dict.values():
        my_list[0] = round(my_list[0], 0)
        my_list[1] = round(my_list[1] / my_list[0], 2)
        my_list[2] = round(my_list[2] / my_list[0], 2)

    return manufacturer_dict


def get_dict_manufacturers_sold():
    manufacturer_dict = {}
    sheet = xlrd.open_workbook(MASTER_TABLE).sheet_by_index(0)
    for i in range(sheet.nrows):
        if i == 0:
            continue

        make = sheet.cell_value(i, MAKE_COL)
        last_date = sheet.cell_value(i, LAST_DATE_COL)
        duration = int(sheet.cell_value(i, DURATION_COL))
        price = sheet.cell_value(i, PRICE_COL)

        if not price or price == 'N/A':
            continue

        if CURR_DATE().strftime(DATE_FORMAT) == last_date:
            continue
        elif make not in manufacturer_dict.keys():
            manufacturer_dict[make] = [1, float(price), duration]
        else:
            my_list = manufacturer_dict[make]
            my_list[0] += 1
            my_list[1] += float(price)
            my_list[2] += duration

    for my_list in manufacturer_dict.values():
        my_list[0] = round(my_list[0], 0)
        my_list[1] = round(my_list[1] / my_list[0], 2)
        my_list[2] = round(my_list[2] / my_list[0], 2)

    return manufacturer_dict


def dealer_cell_format(workbook, worksheet, num_rows):
    worksheet.set_column(0, 0, 2 * DEFAULT_ROW_WIDTH)
    worksheet.set_default_row(DEFAULT_ROW_WIDTH)

    DEALER_SHEET_COND_FORMAT_1['format'] = workbook.add_format(CELL_FORMAT_1)
    DEALER_SHEET_COND_FORMAT_2['format'] = workbook.add_format(CELL_FORMAT_2)

    worksheet.conditional_format(f'B2:B{num_rows}', DEALER_SHEET_COND_FORMAT_1)
    worksheet.conditional_format(f'B2:B{num_rows}', DEALER_SHEET_COND_FORMAT_2)

    worksheet.conditional_format(f'C2:B{num_rows}', DEALER_SHEET_COND_FORMAT_1)
    worksheet.conditional_format(f'C2:B{num_rows}', DEALER_SHEET_COND_FORMAT_2)


def manufacturer_cell_format(workbook, worksheet, num_rows):
    worksheet.set_default_row(DEFAULT_ROW_WIDTH)

    MANUF_SHEET_COND_FORMAT_1['format'] = workbook.add_format(CELL_FORMAT_1)
    MANUF_SHEET_COND_FORMAT_2['format'] = workbook.add_format(CELL_FORMAT_2)

    worksheet.conditional_format(f'B2:B{str(num_rows)}', MANUF_SHEET_COND_FORMAT_1)
    worksheet.conditional_format(f'B2:B{str(num_rows)}', MANUF_SHEET_COND_FORMAT_2)

    worksheet.conditional_format(f'C2:B{str(num_rows)}', MANUF_SHEET_COND_FORMAT_1)
    worksheet.conditional_format(f'C2:B{str(num_rows)}', MANUF_SHEET_COND_FORMAT_2)

    worksheet.conditional_format(f'D2:B{str(num_rows)}', MANUF_SHEET_COND_FORMAT_1)
    worksheet.conditional_format(f'D2:B{str(num_rows)}', MANUF_SHEET_COND_FORMAT_2)

    worksheet.conditional_format(f'E2:B{str(num_rows)}', MANUF_SHEET_COND_FORMAT_1)
    worksheet.conditional_format(f'E2:B{str(num_rows)}', MANUF_SHEET_COND_FORMAT_2)
