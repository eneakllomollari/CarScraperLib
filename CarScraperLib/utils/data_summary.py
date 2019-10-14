import datetime

import pandas
import xlrd

from ..consts import DATE_FORMAT, CELL_FORMAT_1, CELL_FORMAT_2, MANUFACTURER_SHEET_COND_FORMAT_1, \
    MANUFACTURER_SHEET_COND_FORMAT_2, NUM_CARS_HEADER, AVG_DURATION_HEADER, AVG_PRICE_HEADER, DEALER_SHEET_NAME, \
    MANUFACTURER_SHEET_NAME, MAKE_COL, LAST_DATE_COL, DURATION_COL, PRICE_COL, DEALER_SHEET_COND_FORMAT_1, \
    DEALER_SHEET_COND_FORMAT_2, DEFAULT_ROW_WIDTH, DEALER_NAME_COL, NOT_APPLICABLE


def summarize(master_table_loc, summary_all, summary_sold):
    """
    :param master_table_loc: location of the master_table excel
    :param summary_all: where to save the summary for all cars
    :param summary_sold: where the save the summary of sold cars
    """
    writer_all = pandas.ExcelWriter(summary_all, engine='xlsxwriter')
    writer_sold = pandas.ExcelWriter(summary_sold, engine='xlsxwriter')

    _dealer_all(master_table_loc, writer_all)
    _manufacturer_all(master_table_loc, writer_all)
    writer_all.save()

    _dealer_sold(master_table_loc, writer_sold)
    _manufacturer_sold(master_table_loc, writer_sold)
    writer_sold.save()


def _dealer_sold(master_table_loc, writer):
    dealer_dict = get_dict_dealers_sold(master_table_loc)
    dealer_df = pandas.DataFrame(dealer_dict, index=[NUM_CARS_HEADER, AVG_DURATION_HEADER]).transpose()
    dealer_df.to_excel(writer, sheet_name=DEALER_SHEET_NAME)

    _dealer_cell_format(writer.book, writer.sheets[DEALER_SHEET_NAME], len(dealer_dict) + 1)


def _dealer_all(master_table_loc, writer):
    dealer_dict = get_dict_dealers_all(master_table_loc)
    dealer_df = pandas.DataFrame(dealer_dict, index=[NUM_CARS_HEADER, AVG_DURATION_HEADER]).transpose()
    dealer_df.to_excel(writer, sheet_name=DEALER_SHEET_NAME)

    _dealer_cell_format(writer.book, writer.sheets[DEALER_SHEET_NAME], len(dealer_dict) + 1)


def _manufacturer_all(master_table_loc, writer):
    my_dict = get_dict_manufacturers_all(master_table_loc)

    data_frame = pandas.DataFrame(my_dict, index=[NUM_CARS_HEADER, AVG_PRICE_HEADER, AVG_DURATION_HEADER]).transpose()
    data_frame.to_excel(writer, sheet_name=MANUFACTURER_SHEET_NAME)

    _manufacturer_cell_format(writer.book, writer.sheets[MANUFACTURER_SHEET_NAME], len(my_dict) + 1)


def _manufacturer_sold(master_table_loc, writer):
    my_dict = get_dict_manufacturers_sold(master_table_loc)
    data_frame = pandas.DataFrame(my_dict, index=[NUM_CARS_HEADER, AVG_PRICE_HEADER, AVG_DURATION_HEADER]).transpose()
    data_frame.to_excel(writer, sheet_name=MANUFACTURER_SHEET_NAME)

    _manufacturer_cell_format(writer.book, writer.sheets[MANUFACTURER_SHEET_NAME], len(my_dict) + 1)


def get_dict_dealers_all(master_table_loc):
    dealer_dict = {}
    sheet = xlrd.open_workbook(master_table_loc).sheet_by_index(0)

    for i in range(sheet.nrows):
        if i == 0:
            continue
        dealer_name, duration = sheet.cell_value(i, DEALER_NAME_COL), sheet.cell_value(i, DURATION_COL)
        if dealer_name not in dealer_dict.keys():
            dealer_dict[dealer_name] = [1, duration]
        else:
            dealer_dict[dealer_name][0] += 1
            dealer_dict[dealer_name][1] += duration
    return _update_dealer_dict(dealer_dict)


def get_dict_dealers_sold(master_table_loc):
    dealer_dict = {}
    sheet = xlrd.open_workbook(master_table_loc).sheet_by_index(0)

    for i in range(sheet.nrows):
        if i == 0:
            continue
        dealer_name, last_date = sheet.cell_value(i, DEALER_NAME_COL), sheet.cell_value(i, LAST_DATE_COL)
        duration = int(sheet.cell_value(i, DURATION_COL))

        if datetime.datetime.now().strftime(DATE_FORMAT) == last_date:
            continue
        elif dealer_name not in dealer_dict.keys():
            dealer_dict[dealer_name] = [1, duration]
        else:
            dealer_dict[dealer_name][0] += 1
            dealer_dict[dealer_name][1] += duration
    return _update_dealer_dict(dealer_dict)


def get_dict_manufacturers_all(master_table_loc):
    manufacturer_dict = {}
    sheet = xlrd.open_workbook(master_table_loc).sheet_by_index(0)

    for i in range(sheet.nrows):
        if i == 0:
            continue
        make, duration = sheet.cell_value(i, MAKE_COL), int(sheet.cell_value(i, DURATION_COL))
        price = sheet.cell_value(i, PRICE_COL)
        if not price or price == NOT_APPLICABLE:
            continue

        if make not in manufacturer_dict.keys():
            manufacturer_dict[make] = [1, float(price), duration]
        else:
            manufacturer_dict[make][0] += 1
            manufacturer_dict[make][1] += float(price)
            manufacturer_dict[make][2] += duration
    return _update_manufacturer_dict(manufacturer_dict)


def get_dict_manufacturers_sold(master_table_loc):
    manufacturer_dict = {}
    sheet = xlrd.open_workbook(master_table_loc).sheet_by_index(0)
    for i in range(sheet.nrows):
        if i == 0:
            continue
        make, last_date = sheet.cell_value(i, MAKE_COL), sheet.cell_value(i, LAST_DATE_COL)
        duration, price = int(sheet.cell_value(i, DURATION_COL)), sheet.cell_value(i, PRICE_COL)
        if not price or price == 'N/A':
            continue

        if datetime.datetime.now().strftime(DATE_FORMAT) == last_date:
            continue
        elif make not in manufacturer_dict.keys():
            manufacturer_dict[make] = [1, float(price), duration]
        else:
            my_list = manufacturer_dict[make]
            my_list[0] += 1
            my_list[1] += float(price)
            my_list[2] += duration
    return _update_manufacturer_dict(manufacturer_dict)


def _update_manufacturer_dict(manufacturer_dict):
    for my_list in manufacturer_dict.values():
        my_list[0] = round(my_list[0], 0)
        my_list[1] = round(my_list[1] / my_list[0], 2)
        my_list[2] = round(my_list[2] / my_list[0], 2)
    return manufacturer_dict


def _update_dealer_dict(dealer_dict):
    for my_list in dealer_dict.values():
        my_list[1] = round(my_list[1] / my_list[0], 2)
    return dealer_dict


def _dealer_cell_format(workbook, worksheet, num_rows):
    worksheet.set_column(0, 0, 2 * DEFAULT_ROW_WIDTH)
    worksheet.set_default_row(DEFAULT_ROW_WIDTH)

    DEALER_SHEET_COND_FORMAT_1['format'] = workbook.add_format(CELL_FORMAT_1)
    DEALER_SHEET_COND_FORMAT_2['format'] = workbook.add_format(CELL_FORMAT_2)

    worksheet.conditional_format(f'B2:B{num_rows}', DEALER_SHEET_COND_FORMAT_1)
    worksheet.conditional_format(f'B2:B{num_rows}', DEALER_SHEET_COND_FORMAT_2)

    worksheet.conditional_format(f'C2:B{num_rows}', DEALER_SHEET_COND_FORMAT_1)
    worksheet.conditional_format(f'C2:B{num_rows}', DEALER_SHEET_COND_FORMAT_2)


def _manufacturer_cell_format(workbook, worksheet, num_rows):
    worksheet.set_default_row(DEFAULT_ROW_WIDTH)

    MANUFACTURER_SHEET_COND_FORMAT_1['format'] = workbook.add_format(CELL_FORMAT_1)
    MANUFACTURER_SHEET_COND_FORMAT_2['format'] = workbook.add_format(CELL_FORMAT_2)

    worksheet.conditional_format(f'B2:B{str(num_rows)}', MANUFACTURER_SHEET_COND_FORMAT_1)
    worksheet.conditional_format(f'B2:B{str(num_rows)}', MANUFACTURER_SHEET_COND_FORMAT_2)

    worksheet.conditional_format(f'C2:B{str(num_rows)}', MANUFACTURER_SHEET_COND_FORMAT_1)
    worksheet.conditional_format(f'C2:B{str(num_rows)}', MANUFACTURER_SHEET_COND_FORMAT_2)

    worksheet.conditional_format(f'D2:B{str(num_rows)}', MANUFACTURER_SHEET_COND_FORMAT_1)
    worksheet.conditional_format(f'D2:B{str(num_rows)}', MANUFACTURER_SHEET_COND_FORMAT_2)

    worksheet.conditional_format(f'E2:B{str(num_rows)}', MANUFACTURER_SHEET_COND_FORMAT_1)
    worksheet.conditional_format(f'E2:B{str(num_rows)}', MANUFACTURER_SHEET_COND_FORMAT_2)
