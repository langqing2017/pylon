# -*- coding: utf-8 -*-

"""
Store Init
Created on 2019/11/16
@author: langqing2017
@group : pylon
"""

from pylon.store.csv import CsvDataStore
from pylon.stone import StoneHandler

if __name__ == "__main__":
    s = CsvDataStore("./", "data")
    h = StoneHandler(s)
    h.update_store()
