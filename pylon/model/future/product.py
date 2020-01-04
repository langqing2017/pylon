# -*- coding: utf-8 -*-

"""
Future Product
Created on 2019/12/28
@author: langqing2017
@group : pylon
"""

from pylon.model.future.typepath import *

class FutureProduct(object):
    @staticmethod
    def typepath():
        return TypePath_Future_Product

    @staticmethod
    def column_size():
        return 5

    @staticmethod
    def column_types():
        return ["string", "string", "string", "float", "int"]

    def __init__(self, exchange, code, name, price_tick, volume_multiple):
        self.exchange = exchange
        self.code = code
        self.name = name
        self.price_tick = price_tick
        self.volume_multiple = volume_multiple

    def __repr__(self):
        return "%s_%s_%s_%.4f_%d" % (self.exchange, self.code, self.name, self.price_tick, self.volume_multiple)
