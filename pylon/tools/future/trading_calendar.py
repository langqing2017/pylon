# -*- coding: utf-8 -*-

"""
Tools for Future Trading Calendar
Created on 2020/1/5
@author: langqing2017
@group : pylon
"""

from pylon.model.future import FutureTradingCalendar

def get_all_future_trading_calendar(store):
    return store.get_all(FutureTradingCalendar, [])

