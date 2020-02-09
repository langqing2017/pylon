# -*- coding: utf-8 -*-

"""
Data Type Definition
Created on 2019/12/15
@author: langqing2017
@group : pylon
"""

from pylon.model.typepath import *

TypePath_Bond_Instrument = extend_typepath(TypePath_Bond, "ins")
TypePath_Bond_BarData = extend_typepath(TypePath_Bond, "bar")
