# -*- coding: utf-8 -*-

"""
Future Trading Calendar
Created on 2019/12/15
@author: langqing2017
@group : pylon
"""

from pylon.model.future.typepath import *

class FutureTradingCalendar(object):
    @staticmethod
    def typepath():
        return TypePath_Future_TradingCalendar

    @staticmethod
    def column_size():
        return 3

    @staticmethod
    def column_types():
        return ["string", "string", "bool"]

    def __init__(self, exchange, trading_day, is_trading):
        self.exchange = exchange
        self.trading_day = trading_day
        self.is_trading = is_trading

    def __repr__(self):
        return "%s_%s_%s" % (self.exchange, self.trading_day, self.is_trading)
