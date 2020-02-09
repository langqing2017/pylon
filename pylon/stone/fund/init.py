# -*- coding: utf-8 -*-

"""
Fund Init
Created on 2020/2/8
@author: langqing2017
@group : pylon
"""

import os
import os.path
import datetime
from pylon.model.fund import FundBarData, FundInstrument, FundNetValue
from pylon.stone.fund.fetch_fund_nv import *

def init_fund_instrument_and_nv(store):
    instruments, nv_map = fetch_fund_instrument_and_nv()
    store.write_all(instruments, FundInstrument)
    for instrument_id, nv in nv_map.items():
        store.write_all([nv], FundNetValue, ["1d", instrument_id])
