# -*- coding: utf-8 -*-

"""
Stock Instrument
Created on 2019/12/28
@author: langqing2017
@group : pylon
"""

from pylon.model.stock.typepath import *

class StockInstrument(object):
    @staticmethod
    def typepath():
        return TypePath_Stock_Instrument

    @staticmethod
    def column_size():
        return len(StockInstrument.column_types())

    @staticmethod
    def column_types():
        return ["string", "string", "string", "string", "string"]

    def __init__(self, id, exchange, market, code, name):
        self.id = id
        self.exchange = exchange
        self.market = market
        self.code = code
        self.name = name

    def __repr__(self):
        return "%s_%s_%s_%s_%s" % (self.id, self.exchange, self.market, self.code, self.name)
