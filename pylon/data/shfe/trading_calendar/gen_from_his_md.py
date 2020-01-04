# -*- coding: utf-8 -*-

"""
Generate Trading Calendar with data in shfe/history_md
Created on 2019/12/15
@author: langqing2017
@group : pylon
"""

import os
import sys
import xlrd
import re

regex_date = "^\d{8}$"

def get_trading_day_list(filepath):
    wb = xlrd.open_workbook(filepath)
    ws = wb.sheet_by_index(0)
    date_set = set()
    for row in range(3, ws.nrows):     #skip the first three rows
        date = ws.cell(row, 1).value
        if re.match(regex_date, date):
            date_set.add(date)
    return sorted(date_set)

if __name__ == "__main__":
    for year in range(2010, 2019):
        path = os.path.join(os.path.dirname(sys.argv[0]), "../history_md/history_md_%d.xls" % year)
        date_list = get_trading_day_list(path)
        print("parse trading calendar ok: %d" % year)
        
        path = os.path.join(os.path.dirname(sys.argv[0]), "trading_calendar_%d.csv" % year)
        f = open(path, "w")
        for date in date_list:
            f.write("%s\n" % date)
        f.close()
        print("write trading calendar ok: %d" % year)
