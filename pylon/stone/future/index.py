# -*- coding: utf-8 -*-

"""
Future Index
Created on 2019/12/28
@author: langqing2017
@group : pylon
"""

from pylon.model.future import FutureBarData

def gen_future_index_EI(product, ins_list, store):
    print("generating index_EI for %s..." % product)

    trading_day_set = set()
    data_map_list = []
    for ins in ins_list:
        data_list = store.get_all(FutureBarData, ["1d", ins.code])
        data_map = {}
        for data in data_list:
            data_map[data.time] = data
        data_map_list.append(data_map)
        trading_day_set.update(data_map.keys())

    data_list = []
    for trading_day in sorted(trading_day_set):
        # print("caculating closep for %s %s..." % (product, trading_day.strftime("%Y%m%d")))
        total_m = 0.0
        total_p = 0.0
        total_v = 0.0
        close_price = 0.0
        for data_map in data_map_list:
            if trading_day in data_map:
                close_price = data_map[trading_day].close_price
                total_m += data_map[trading_day].close_price * data_map[trading_day].position
                total_p += data_map[trading_day].position
                total_v += data_map[trading_day].volumn
        if total_p != 0:
            close_price = total_m / total_p
        data = FutureBarData(trading_day, close_price, close_price, close_price, \
                close_price, close_price, close_price, close_price, total_v, total_m, total_p)
        data_list.append(data)
    store.write_all(data_list, FutureBarData, ["1d", "%sEI" % product])
