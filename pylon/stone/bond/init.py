# -*- coding: utf-8 -*-

"""
Bond Init
Created on 2020/2/8
@author: langqing2017
@group : pylon
"""

import os
import os.path
import datetime
from pylon.model.bond import BondBarData, BondInstrument
from pylon.stone.bond.fetch_bond_bardata import *

def init_bond_instrument_and_bardata(store):
    instruments, bardata_map = fetch_bond_instrument_and_bardata()
    store.write_all(instruments, BondInstrument)
    for instrument_id, bardata in bardata_map.items():
        store.write_all([bardata], BondBarData, ["1d", instrument_id])
