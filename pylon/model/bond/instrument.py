# -*- coding: utf-8 -*-

"""
Bond Instrument
Created on 2020/2/8
@author: langqing2017
@group : pylon
"""

from pylon.model.bond.typepath import *

class BondInstrument(object):
    @staticmethod
    def typepath():
        return TypePath_Bond_Instrument

    @staticmethod
    def column_size():
        return len(BondInstrument.column_types())

    @staticmethod
    def column_types():
        return ["string", "string", "string", "string", "string"]

    def __init__(self, id, exchange, category, code, name):
        self.id = id
        self.exchange = exchange
        self.category = category
        self.code = code
        self.name = name

    def __repr__(self):
        return "%s_%s_%s_%s_%s" % (self.id, self.exchange, self.category, self.code, self.name)
