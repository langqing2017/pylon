# -*- coding: utf-8 -*-

"""
Fund Update
Created on 2020/2/8
@author: langqing2017
@group : pylon
"""

import os
import os.path
import datetime
from pylon.model.fund import FundBarData, FundInstrument
from pylon.stone.fund.fetch_fund_nv import *
from pylon.stone.fund.fetch_fund_bardata import *

def update_fund_instrument_and_nv_and_bardata(store):
    instruments, nv_map = fetch_fund_instrument_and_nv()
    store.write_all(instruments, FundInstrument)
    for instrument_id, nv in nv_map.items():
        store.append(nv, FundNetValue, ["1d", instrument_id])

    bardata_map = fetch_fund_bardata()
    for instrument_id, bardata in bardata_map.items():
        store.append(bardata_map, FundBarData, ["1d", instrument_id])
