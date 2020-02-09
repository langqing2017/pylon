# -*- coding: utf-8 -*-

"""
Stock Init
Created on 2020/2/8
@author: langqing2017
@group : pylon
"""

import os
import os.path
import datetime
from pylon.model.stock import StockTradingCalendar, StockBarData, StockInstrument
from pylon.stone.stock.fetch_stock_bardata import *

def init_stock_trading_calendar(store, datadir):
    path = os.path.join(datadir, "shfe/trading_calendar/trading_calendar_%d.csv")
    trading_day_set = set()
    for year in range(2010, 2021):
        f = open(path % year)
        for line in f.readlines():
            if line.strip() == "":
                continue
            trading_day_set.add(line.strip())
    
    items = []
    date = datetime.date(2010, 1, 1)
    end = datetime.date(2021, 1, 1)
    while date < end:
        datestr = date.strftime("%Y%m%d")
        if datestr in trading_day_set:
            items.append(StockTradingCalendar("SSE", datestr, True))
        else:
            items.append(StockTradingCalendar("SSE", datestr, False))
        date = date + datetime.timedelta(days=1)

    store.write_all(items, StockTradingCalendar)

def init_stock_instrument_and_bardata(store):
    instruments, bardata_map = fetch_stock_instrument_and_bardata()
    store.write_all(instruments, StockInstrument)
    for instrument_id, bardata in bardata_map.items():
        store.write_all([bardata], StockBarData, ["1d", instrument_id])
