# -*- coding: utf-8 -*-

"""
Data Type Definition
Created on 2019/12/15
@author: langqing2017
@group : pylon
"""

from pylon.model.typepath import *

TypePath_Future_TradingCalendar = extend_typepath(TypePath_Future, "tc")
TypePath_Future_Product = extend_typepath(TypePath_Future, "pdt")
TypePath_Future_Instrument = extend_typepath(TypePath_Future, "ins")
TypePath_Future_Index = extend_typepath(TypePath_Future, "idx")
TypePath_Future_BarData = extend_typepath(TypePath_Future, "bar")
