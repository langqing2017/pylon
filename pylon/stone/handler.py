# -*- coding: utf-8 -*-

"""
Stone Handler
Created on 2019/11/16
@author: langqing2017
@group : pylon
"""

import os.path
from pylon.stone.future import *

PYLON_DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../data")

class StoneHandler():

    def __init__(self, store):
        self.__store = store

    def init_store(self):
        self.init_future()
        self.generate_future_index()

    def init_future(self):
        init_future_trading_calendar(self.__store, PYLON_DATA_PATH)
        init_future_product(self.__store, PYLON_DATA_PATH)

        ins_list = []
        init_future_bar_1d_shfe(self.__store, PYLON_DATA_PATH, ins_list)
        init_future_bar_1d_dce(self.__store, PYLON_DATA_PATH, ins_list)
        init_future_bar_1d_czce(self.__store, PYLON_DATA_PATH, ins_list)
        ins_list.sort(key=str)
        self.__store.write_all(ins_list, FutureInstrument)

    def generate_future_index(self):
        ins_list = self.__store.get_all(FutureInstrument)
        product_map = {}
        for ins in ins_list:
            if ins.product not in product_map:
                product_map[ins.product] = []
            product_map[ins.product].append(ins)

        for product,ins_list in product_map.items():
            gen_future_index_EI(product, ins_list, self.__store)
