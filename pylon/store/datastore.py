# -*- coding: utf-8 -*-

"""
Data Store Definition
Created on 2019/11/16
@author: langqing2017
@group : pylon
"""

class DataStore(object):
    def get_all(self, type, keys = []):
        raise NotImplementedError()

    def get_last(self, type, keys = []):
        raise NotImplementedError()

    def append(self, data, type, keys = []):
        raise NotImplementedError()

    def append_all(self, list, type, keys = []):
        raise NotImplementedError()

    def write_all(self, list, type, keys = []):
        raise NotImplementedError()
