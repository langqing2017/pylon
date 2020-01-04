# -*- coding: utf-8 -*-

"""
Generate Trading Calendar for workday
Created on 2019/12/15
@author: langqing2017
@group : pylon
"""

import os
import sys
import datetime

def gen_trading_day_list(year):
    first_day = datetime.datetime(year, 1, 1)
    date_list = []
    for delta in range(0, 366):
        date = first_day + datetime.timedelta(days=delta)
        if date.year != year:
            continue
        if date.weekday() >= 5:
            continue
        date_list.append(date.strftime("%Y%m%d"))
    return date_list

if __name__ == "__main__":
    for year in range(2019, 2021):
        date_list = gen_trading_day_list(year)
        print("generate trading calendar ok: %d" % year)

        path = os.path.join(os.path.dirname(sys.argv[0]), "trading_calendar_%d.csv" % year)
        f = open(path, "w")
        for date in date_list:
            f.write("%s\n" % date)
        f.close()
        print("write trading calendar ok: %d" % year)
