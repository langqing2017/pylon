# -*- coding: utf-8 -*-

"""
Data Type Definition
Created on 2019/12/15
@author: langqing2017
@group : pylon
"""

from pylon.model.typepath import *

TypePath_Stock_TradingCalendar = extend_typepath(TypePath_Stock, "tc")
TypePath_Stock_Instrument = extend_typepath(TypePath_Stock, "ins")
TypePath_Stock_Index = extend_typepath(TypePath_Stock, "idx")
TypePath_Stock_BarData = extend_typepath(TypePath_Stock, "bar")
