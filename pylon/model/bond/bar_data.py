# -*- coding: utf-8 -*-

"""
Bond Bar Data
Created on 2020/2/8
@author: langqing2017
@group : pylon
"""

from pylon.model.bond.typepath import *

class BondBarData(object):
    @staticmethod
    def typepath():
        return TypePath_Bond_BarData

    @staticmethod
    def column_size():
        return len(BondBarData.column_types())

    @staticmethod
    def column_types():
        return ["datetime", "float", "float", "float", "float", "float", "int", "float"]

    def __init__(self, time, open_price, high_price, low_price, close_price, pre_close_price, volumn, money):
        self.time = time
        self.open_price = open_price
        self.high_price = high_price
        self.low_price = low_price
        self.close_price = close_price
        self.pre_close_price = pre_close_price
        self.volumn = volumn
        self.money = money

    def __repr__(self):
        return "%s_%.4f_%.4f_%.4f_%.4f_%.4f_%d_%.4f" % \
                (self.time.strftime("%Y%m%d%H%M%S"), self.open_price, self.high_price, self.low_price, \
                self.close_price, self.pre_close_price, self.volumn, self.money)
