import os
import csv
import string

from datetime import datetime

from core.config import settings as env_settings


date_format = "%d/%m/%Y "


def set_format(value):
    if value and type(value) is datetime:
        return "{}".format(value.strftime(date_format))

    return "{}".format(value) if value else ''

def set_format_2(value):
    date_format = "%Y-%m-%d %H:%M:%S"
    if value and type(value) is datetime:
        return "{}".format(value.strftime(date_format))

    return "{}".format(value) if value else ''

def set_upper_format(value):
    return "{}".format(value.upper()) if value else ''


def get_columnletter_alias(value):
    column_alp = 27


    col_alias = "{}"

    if value > column_alp:
        col_alias = "A{}"
        value = value - 1 - column_alp
    else:
        value = value - 1

    return col_alias.format(string.ascii_uppercase[value])


def get_state_sheet_id(state):
    return STATES_SHEET.get(state)


def get_all_states():
    return STATES_SHEET.keys()


def sheet_ranges(headers, data):
    # Set the headers
    col_size = len(headers)
    alias_col = get_columnletter_alias(col_size)
    range_headers = 'A1:{}1'.format(alias_col)

    # Set the results
    row_size = len(data)
    index_results = 2
    tot_results = row_size + index_results
    range_results = 'A{}:{}{}'.format(
        index_results,
        alias_col,
        tot_results
    )

    return range_headers, range_results


def write_file_report(item):
    path = ""
    csv_file = open(path, 'a')
    writer = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
    writer.writerow([
        item.get('FECHA'),
        item.get('EVENTO'),
        item.get('STATUS')
    ])
    csv_file.close()

def set_dic_list(listof_lists:list, headers:list): 
    dic_list = []

    for row in listof_lists:
        aux_dict = {}
        for column in range(len(row)):
            aux_dict[headers[column]] = row[column]
        dic_list.append(aux_dict)
            
    return dic_list