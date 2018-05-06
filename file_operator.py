#encoding:utf-8
import csv
import codecs

import sys

from openpyxl import Workbook
from openpyxl import load_workbook

workbook = Workbook()
booksheet_w = workbook.active

workbook_r = load_workbook('800.xlsx')
sheets = workbook_r.sheetnames
booksheet = workbook_r[sheets[0]]
rows = booksheet.rows
for row in booksheet.rows:
    for cell in row:
        print (cell.value)

booksheet_w.append(["啊大叔?","放大放大"])
booksheet_w.append(["阿达达","阿达达"])
booksheet_w.append(["english","123"])
workbook.save("test_openpyxl.xlsx")
