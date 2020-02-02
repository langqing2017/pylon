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
        data_list = store.get_all(FutureBarData, ["1d", ins.id])
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

def gen_future_index_GI(product, ins_list, store):
    print("generating index_GI for %s..." % product)

    trading_day_set = set()
    data_maps = {}
    for ins in ins_list:
        data_list = store.get_all(FutureBarData, ["1d", ins.id])
        data_map = {}
        for data in data_list:
            data_map[data.time] = data
        data_maps[ins.id] = data_map
        trading_day_set.update(data_map.keys())

    last_main_instrument_id = None
    main_instrument_map = {}
    for trading_day in sorted(trading_day_set):
        max_position = -1
        main_instrument_id = None
        for instrument_id in data_maps.keys():
            data_map = data_maps[instrument_id]
            if trading_day in data_map:
                if max_position < data_map[trading_day].position:
                    max_position = data_map[trading_day].position
                    main_instrument_id = instrument_id

        if main_instrument_id != None:
            if last_main_instrument_id == None or last_main_instrument_id < main_instrument_id:
                #change
                main_instrument_map[trading_day] = main_instrument_id
                last_main_instrument_id = main_instrument_id
            else:
                main_instrument_map[trading_day] = last_main_instrument_id
        else:
            print("error: can't find main for %s, %s" % (product, trading_day))

    ratio_map = {}
    changing = 0
    last_main_instrument_id = None
    for trading_day in sorted(trading_day_set):
        if trading_day not in main_instrument_map:
            continue

        current_main_instrument_id = main_instrument_map[trading_day]
        data_map = data_maps[current_main_instrument_id]
        if (last_main_instrument_id != None and current_main_instrument_id != last_main_instrument_id) or changing > 0:
            #change main
            changing += 1
            ratio = 1.0 if data_map[trading_day].pre_close_price == 0.0 \
                else data_map[trading_day].close_price / data_map[trading_day].pre_close_price
            data_map2 = data_maps[last_main_instrument_id]
            if trading_day in data_map2:
                ratio2 = 1.0 if data_map2[trading_day].pre_close_price == 0.0 \
                    else data_map2[trading_day].close_price / data_map2[trading_day].pre_close_price
                ratio_map[trading_day] = changing * ratio / 3.0 + (3.0 - changing) * ratio2 / 3.0
            else:
                ratio_map[trading_day] = ratio
                changing = 3
            if changing >= 3:
                changing = 0
                last_main_instrument_id = current_main_instrument_id
        else:
            last_main_instrument_id = current_main_instrument_id
            ratio = 1.0 if data_map[trading_day].pre_close_price == 0.0 \
                else data_map[trading_day].close_price / data_map[trading_day].pre_close_price
            ratio_map[trading_day] = ratio

    #gen index value
    index_value = None
    index_map = {}
    for trading_day in sorted(trading_day_set):
        if index_value == None:
            index_value = 1000.0
        else:
            index_value = index_value * ratio_map[trading_day]
        index_map[trading_day] = index_value

    #get position value = position * close_price
    ei_data_list = store.get_all(FutureBarData, ["1d", "%sEI" % product])
    data_list = []
    for ei_data in ei_data_list:
        trading_day = ei_data.time
        if trading_day not in index_map:
            continue
        position = ei_data.position * ei_data.close_price
        volumn = ei_data.volumn * ei_data.close_price
        close_price = index_map[trading_day]
        data = FutureBarData(trading_day, close_price, close_price, close_price, \
                close_price, close_price, close_price, close_price, volumn, volumn, position)
        data_list.append(data)
    store.write_all(data_list, FutureBarData, ["1d", "%sGI" % product])
