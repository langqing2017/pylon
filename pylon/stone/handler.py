# -*- coding: utf-8 -*-

"""
Stone Handler
Created on 2019/11/16
@author: langqing2017
@group : pylon
"""

import os.path
from pylon.stone.future import *
from pylon.stone.stock import *
from pylon.stone.fund import *
from pylon.stone.bond import *

PYLON_DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../data")

class StoneHandler():

    def __init__(self, store):
        self.__store = store

    def init_store(self):
        # # future
        self.init_future()
        self.generate_future_index()

        # # stock
        init_stock_trading_calendar(self.__store, PYLON_DATA_PATH)
        init_stock_instrument_and_bardata(self.__store)

        # fund
        init_fund_instrument_and_nv(self.__store)

        # bond
        init_bond_instrument_and_bardata(self.__store)

    def update_store(self):
        # future
        self.update_future()
        self.generate_future_index()

        # stock
        update_stock_instrument_and_bardata(self.__store)

        # fund
        update_fund_instrument_and_nv_and_bardata(self.__store)

        # bond
        update_bond_instrument_and_bardata(self.__store)

    def init_future(self):
        init_future_trading_calendar(self.__store, PYLON_DATA_PATH)
        init_future_product(self.__store, PYLON_DATA_PATH)

        # clear FutureInstrument
        self.__store.write_all([], FutureInstrument)
        init_future_bar_1d_shfe(self.__store, PYLON_DATA_PATH)
        init_future_bar_1d_dce(self.__store, PYLON_DATA_PATH)
        init_future_bar_1d_czce(self.__store, PYLON_DATA_PATH)

    def update_future(self):
        update_future_bar_1d_shfe(self.__store)
        update_future_bar_1d_dce(self.__store)
        update_future_bar_1d_czce(self.__store)

    def generate_future_index(self):
        ins_list = self.__store.get_all(FutureInstrument)
        product_map = {}
        for ins in ins_list:
            if ins.product not in product_map:
                product_map[ins.product] = []
            product_map[ins.product].append(ins)

        for product,ins_list in product_map.items():
            gen_future_index_EI(product, ins_list, self.__store)
            gen_future_index_GI(product, ins_list, self.__store)

