# -*- coding: utf-8 -*-

"""
Data Type Definition
Created on 2019/12/15
@author: langqing2017
@group : pylon
"""

from pylon.model.typepath import *

TypePath_Fund_Instrument = extend_typepath(TypePath_Fund, "ins")
TypePath_Fund_BarData = extend_typepath(TypePath_Fund, "bar")
TypePath_Fund_NetValue = extend_typepath(TypePath_Fund, "nv")
