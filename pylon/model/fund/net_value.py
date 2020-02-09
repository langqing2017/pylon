# -*- coding: utf-8 -*-

"""
Fund Net Value
Created on 2020/2/8
@author: langqing2017
@group : pylon
"""

from pylon.model.fund.typepath import *

class FundNetValue(object):
    @staticmethod
    def typepath():
        return TypePath_Fund_NetValue

    @staticmethod
    def column_size():
        return len(FundNetValue.column_types())

    @staticmethod
    def column_types():
        return ["date", "float"]

    def __init__(self, date, net_value):
        self.date = date
        self.net_value = net_value

    def __repr__(self):
        return "%s_%.4f" % (self.date.strftime("%Y%m%d"), self.net_value)
