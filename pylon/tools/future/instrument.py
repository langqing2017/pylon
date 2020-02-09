# -*- coding: utf-8 -*-

"""
Tools for Future Instrument
Created on 2020/1/5
@author: langqing2017
@group : pylon
"""

from pylon.model.future import FutureInstrument

def get_all_future_instrument(store):
    return store.get_all(FutureInstrument, [])

def get_instrument_code_set(store):
    instruments = store.get_all(FutureInstrument, [])
    instrument_code_set = set()
    for instrument in instruments:
        instrument_code_set.add(instrument.code)
    return instrument_code_set

def get_product_code(instrument_code):
    if instrument_code[1].isdigit():
        product_code = instrument_code[:1]
    else:
        product_code = instrument_code[:2]
    return product_code

def get_expire_month(instrument_code):
    if instrument_code[1].isdigit():
        expire = instrument_code[1:]
    else:
        expire = instrument_code[2:]
    return expire
