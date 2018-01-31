#!/usr/bin/env python
import json
from optparse import OptionParser

import xlsxwriter


def convert_json_to_xlsx(filename):
    with open(filename) as file:
        data = json.loads(file.read())

    # erase categories
    data = filter(lambda x: 'address' in x, data)

    # Create an new Excel file and add a worksheet.
    workbook = xlsxwriter.Workbook('Excel.xlsx')
    worksheet = workbook.add_worksheet()

    column_widths = [(0, 60), (1, 25), (2, 25), (3, 80)]  # (2, 10), (3, 10)
    for col, width in column_widths:
        worksheet.set_column(firstcol=col, lastcol=col, width=width)

    for row, item in enumerate(data):
        for col, field in enumerate(['name', 'address', 'email', 'rubrics']):  # 'lat', 'lon'
            worksheet.write(row, col, item.get(field))

    workbook.close()


if __name__ == '__main__':

    parser = OptionParser()
    parser.add_option('-f', '--file', dest='filename', help='input/output json file', metavar='FILE')

    (options, args) = parser.parse_args()

    file_name = None
    if len(args) > 0:
        convert_json_to_xlsx(args[0])
    elif options.filename:
        convert_json_to_xlsx(options.filename)
    else:
        print('''Usage: json_to_xlsx.py [options]
Options:
  -h, --help            show this help message and exit
  -f FILE, --file=FILE  input/output file
''')
