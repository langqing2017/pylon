# -*- coding: utf-8 -*-

"""
Data Type Definition
Created on 2019/12/15
@author: langqing2017
@group : pylon
"""

import copy

TypePath_Future = ["fu"]
TypePath_Stock = ["stk"]
TypePath_Fund = ["fund"]
TypePath_Bond = ["bond"]
TypePath_Option = ["opt"]

def extend_typepath(super_typepath, typename):
    typepath = copy.copy(super_typepath)
    typepath.append(typename)
    return typepath
