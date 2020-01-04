# -*- coding: utf-8 -*-

"""
Future Instrument
Created on 2019/12/28
@author: langqing2017
@group : pylon
"""

from pylon.model.future.typepath import *

class FutureInstrument(object):
    @staticmethod
    def typepath():
        return TypePath_Future_Instrument

    @staticmethod
    def column_size():
        return 3

    @staticmethod
    def column_types():
        return ["string", "string", "string"]

    def __init__(self, exchange, product, code):
        self.exchange = exchange
        self.product = product
        self.code = code

    def __repr__(self):
        return "%s_%s_%s" % (self.exchange, self.product, self.code)
