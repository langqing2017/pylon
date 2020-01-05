# -*- coding: utf-8 -*-

"""
Future Update
Created on 2020/1/5
@author: langqing2017
@group : pylon
"""

import datetime
from pylon.tools import future as future_tools
from pylon.model.future import FutureBarData, FutureInstrument
from pylon.stone.future.fetch_daily import *

def update_future_bar_1d_shfe(store):
    product_map = future_tools.get_product_name_code_map(store)
    instrument_set = future_tools.get_instrument_code_set(store)
    last_update = store.get_last_update(FutureBarData, ["1d", "shfe"])
    date_list = future_tools.get_all_future_trading_calendar(store)
    for date in date_list:
        if not date.is_trading:
            continue
        dt = datetime.datetime.strptime(date.trading_day, "%Y%m%d")
        if dt > last_update and dt < datetime.datetime.now():
            md_map = fetch_future_daily_shfe(dt, product_map)
            if len(md_map) <= 0:
                continue
            print("fetch shfe(%s) return %d items" % (date.trading_day, len(md_map)))
            for instrument, md in md_map.items():
                if instrument not in instrument_set:
                    ins = FutureInstrument("shfe", future_tools.get_product_code(instrument), instrument)
                    store.append(ins, FutureInstrument, [])
                    instrument_set.add(instrument)
                store.append(md, FutureBarData, ["1d", instrument])
            store.set_last_update(dt, FutureBarData, ["1d", "shfe"])

def update_future_bar_1d_dce(store):
    product_map = future_tools.get_product_name_code_map(store)
    instrument_set = future_tools.get_instrument_code_set(store)
    last_update = store.get_last_update(FutureBarData, ["1d", "dce"])
    date_list = future_tools.get_all_future_trading_calendar(store)
    for date in date_list:
        if not date.is_trading:
            continue
        dt = datetime.datetime.strptime(date.trading_day, "%Y%m%d")
        if dt > last_update and dt < datetime.datetime.now():
            md_map = fetch_future_daily_dce(dt, product_map)
            if len(md_map) <= 0:
                continue
            print("fetch dce(%s) return %d items" % (date.trading_day, len(md_map)))
            for instrument, md in md_map.items():
                if instrument not in instrument_set:
                    ins = FutureInstrument("dce", future_tools.get_product_code(instrument), instrument)
                    store.append(ins, FutureInstrument, [])
                    instrument_set.add(instrument)
                store.append(md, FutureBarData, ["1d", instrument])
            store.set_last_update(dt, FutureBarData, ["1d", "dce"])

def update_future_bar_1d_czce(store):
    instrument_set = future_tools.get_instrument_code_set(store)
    last_update = store.get_last_update(FutureBarData, ["1d", "czce"])
    date_list = future_tools.get_all_future_trading_calendar(store)
    for date in date_list:
        if not date.is_trading:
            continue
        dt = datetime.datetime.strptime(date.trading_day, "%Y%m%d")
        if dt > last_update and dt < datetime.datetime.now():
            md_map = fetch_future_daily_czce(dt)
            if len(md_map) <= 0:
                continue
            print("fetch czce(%s) return %d items" % (date.trading_day, len(md_map)))
            for instrument, md in md_map.items():
                if instrument not in instrument_set:
                    ins = FutureInstrument("czce", future_tools.get_product_code(instrument), instrument)
                    store.append(ins, FutureInstrument, [])
                    instrument_set.add(instrument)
                store.append(md, FutureBarData, ["1d", instrument])
            store.set_last_update(dt, FutureBarData, ["1d", "czce"])
