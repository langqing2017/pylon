# -*- coding: utf-8 -*-

"""
Csv Data Store
Created on 2019/12/22
@author: langqing2017
@group : pylon
"""

import os.path
from pylon.model import type_convert
from pylon.store import DataStore

class CsvDataStore(DataStore):
    def __init__(self, folder, source):
        self.__folder = folder
        self.__source = source

    def get_filepath(self, type, keys = []):
        if len(keys) == 0:
            filename = "%s.csv" % type.typepath()[-1]
        else:
            filename = "%s.csv" % keys[-1]
        paths = tuple(type.typepath()) + tuple(keys[:-1]) + tuple([filename])
        filepath = os.path.join(self.__folder, self.__source, *paths)
        if not os.path.exists(os.path.dirname(filepath)):
            os.makedirs(os.path.dirname(filepath))
        return filepath

    def get_all(self, type, keys = []):
        filepath = self.get_filepath(type, keys)
        converts = []
        for column_type in type.column_types():
            if column_type == "string":
                converts.append(None)
            else:
                converts.append(getattr(type_convert, "string_to_%s" % column_type))
        rows = []
        with open(filepath, "r") as fp:
            for line in fp:
                ss = line.split(",")
                if len(ss) != type.column_size():
                    continue
                row = []
                for i in range(0, type.column_size()):
                    if converts[i] == None:
                        row.append(ss[i].strip())
                    else:
                        row.append(converts[i](ss[i].strip()))
                args = tuple(row)
                rows.append(type(*args))
        return rows

    def get_last(self, type, keys = []):
        rows = self.get_all(type, keys)
        if len(rows) <= 0:
            return None
        return rows[-1]

    def append(self, data, type, keys = []):
        filepath = self.get_filepath(type, keys)
        with open(filepath, "a") as fp:
            fp.write(str(data).replace("_", ",") + "\n")

    def append_all(self, list, type, keys = []):
        filepath = self.get_filepath(type, keys)
        with open(filepath, "a") as fp:
            for data in list:
                fp.write(str(data).replace("_", ",") + "\n")

    def write_all(self, list, type, keys = []):
        filepath = self.get_filepath(type, keys)
        with open(filepath, "w") as fp:
            for data in list:
                fp.write(str(data).replace("_", ",") + "\n")

if __name__ == "__main__":
    from pylon.model.future import FutureTradingCalendar
    store = CsvDataStore("./", "base")
    rows = store.get_all(FutureTradingCalendar)
    print(rows)

    tc = FutureTradingCalendar("SHFE", "20191224", True)
    store.append(FutureTradingCalendar, tc)
