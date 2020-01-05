# -*- coding: utf-8 -*-

"""
Tools for Future Product
Created on 2020/1/5
@author: langqing2017
@group : pylon
"""

from pylon.model.future import FutureProduct

def get_all_future_product(store):
    return store.get_all(FutureProduct, [])

def get_product_name_code_map(store):
    products = store.get_all(FutureProduct, [])
    product_name_code_map = {}
    for product in products:
        product_name_code_map[product.name] = product.code
    return product_name_code_map

