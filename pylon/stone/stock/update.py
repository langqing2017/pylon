# -*- coding: utf-8 -*-

"""
Stock Update
Created on 2020/2/8
@author: langqing2017
@group : pylon
"""

import os
import os.path
import datetime
from pylon.model.stock import StockTradingCalendar, StockBarData, StockInstrument
from pylon.stone.stock.fetch_stock_bardata import *

def update_stock_instrument_and_bardata(store):
    instruments, bardata_map = fetch_stock_instrument_and_bardata()
    store.write_all(instruments, StockInstrument)
    for instrument_id, bardata in bardata_map.items():
        store.append(bardata, StockBarData, ["1d", instrument_id])
