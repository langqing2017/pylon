# -*- coding: utf-8 -*-

"""
Type Convert
Created on 2019/12/22
@author: langqing2017
@group : pylon
"""

from dateutil import parser

def string_to_int(v):
    return int(v)

def string_to_float(v):
    return float(v)

def string_to_bool(v):
    v = v.lower()
    if v == "y" or v == "yes" or v == "true" or v == "1":
        return True
    return False

def string_to_datetime(v):
    return parser.parse(v)

def string_to_date(v):
    return parser.parse(v)
