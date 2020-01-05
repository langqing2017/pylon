# -*- coding: utf-8 -*-

"""
Future Init
Created on 2019/12/28
@author: langqing2017
@group : pylon
"""

import os
import os.path
import datetime
import xlrd
import zipfile
import shutil
import re
from pylon.model.future import FutureTradingCalendar, FutureProduct, FutureBarData, FutureInstrument

regex_date = "^\d{8}$"

def init_future_trading_calendar(store, datadir):
    path = os.path.join(datadir, "shfe/trading_calendar/trading_calendar_%d.csv")
    trading_day_set = set()
    for year in range(2010, 2020):
        f = open(path % year)
        for line in f.readlines():
            if line.strip() == "":
                continue
            trading_day_set.add(line.strip())
    
    items = []
    date = datetime.date(2010, 1, 1)
    end = datetime.date(2021, 1, 1)
    while date < end:
        datestr = date.strftime("%Y%m%d")
        if datestr in trading_day_set:
            items.append(FutureTradingCalendar("SHFE", datestr, True))
        else:
            items.append(FutureTradingCalendar("SHFE", datestr, False))
        date = date + datetime.timedelta(days=1)

    store.write_all(items, FutureTradingCalendar)

def init_future_product(store, datadir):
    path = os.path.join(datadir, "future_product.csv")
    items = []
    with open(path) as fp:
        for line in fp.readlines():
            ss = line.strip().split(",")
            if len(ss) != FutureProduct.column_size():
                continue
            exchange = ss[0].strip()
            code = ss[1].strip()
            name = ss[2].strip()
            price_tick = float(ss[3].strip())
            volume_multiple = int(ss[4].strip())
            items.append(FutureProduct(exchange, code, name, price_tick, volume_multiple))
    store.write_all(items, FutureProduct)

def __parse_float(str, value):
    if str == "" or str == "0":
        return value
    return float(str)

def init_future_bar_1d_shfe(store, datadir):
    path = os.path.join(datadir, "shfe/history_md/history_md_%d.xls")
    ins_list = []
    md_map = {}
    for year in range(2010, 2019):
        wb = xlrd.open_workbook(path % year)
        print("parsing %d" % year)
        ws = wb.sheet_by_index(0)
        last_instrument = ""
        for row in range(3, ws.nrows):     #skip the first three rows
            instrument = ws.cell(row, 0).value
            if instrument == "":
                instrument = last_instrument
            else:
                last_instrument = instrument
            date = ws.cell(row, 1).value
            if not re.match(regex_date, date):
                continue
            if len(instrument) > 6:
                continue
            time = datetime.datetime.strptime(date, "%Y%m%d")
            pre_close_price = float(ws.cell(row, 2).value)
            pre_clear_price = float(ws.cell(row, 3).value)
            open_price = __parse_float(ws.cell(row, 4).value, pre_clear_price)
            high_price = __parse_float(ws.cell(row, 5).value, pre_clear_price)
            low_price = __parse_float(ws.cell(row, 6).value, pre_clear_price)
            close_price = __parse_float(ws.cell(row, 7).value, pre_clear_price)
            clear_price = float(ws.cell(row, 8).value)
            volumn = int(ws.cell(row, 11).value)
            money = float(ws.cell(row, 12).value)
            position = float(ws.cell(row, 13).value)
            data = FutureBarData(time, open_price, high_price, low_price, \
                close_price, clear_price, pre_close_price, pre_clear_price, volumn, money, position)
            
            if instrument not in md_map:
                md_map[instrument] = []
            md_map[instrument].append(data)

    for instrument, items in md_map.items():
        items.sort(key=lambda x:x.time)
        store.write_all(items, FutureBarData, ["1d", instrument])

        product = instrument[:2]
        ins = FutureInstrument("SHFE", product, instrument)
        ins_list.append(ins)
    
    ins_list.sort(key=str)
    store.append_all(ins_list, FutureInstrument)
    store.set_last_update(datetime.datetime.strptime("20190101", "%Y%m%d"), FutureBarData, ["1d", "shfe"])

def __parse_future_bar_1d_dce_zip(datadir, products, md_map):
    path = os.path.join(datadir, "dce/history_md/history_md_%d_%s.zip")
    newpath = os.path.join(datadir, "dce/history_md/unzip/history_md_%d_%s.csv")
    tmpdir = os.path.join(datadir, "dce/history_md/unzip")
    if not os.path.exists(tmpdir):
        os.makedirs(tmpdir)
    for year in range(2010, 2017):
        for product in products:
            if product.exchange != "DCE":
                continue
            filename = path % (year, product.code)
            newfilename = newpath % (year, product.code)
            if not os.path.exists(filename):
                continue
            print("processing %s" % filename)
            zfile = zipfile.ZipFile(filename)
            for fn in zfile.namelist():
                right_fn = fn.encode("cp437").decode('gbk')
                with open(newfilename, 'wb') as output_file:
                    with zfile.open(fn, 'r') as origin_file:
                        shutil.copyfileobj(origin_file, output_file)

            with open(newfilename, "r", encoding="gbk") as fp:
                for line in fp.readlines()[1:]:
                    ss = line.split(",")
                    if len(ss) != 15:
                        continue
                    instrument = ss[1].replace("\"", "")
                    date = ss[2].replace("\"", "")
                    time = datetime.datetime.strptime(date, "%Y%m%d")
                    pre_clear_price = float(ss[4].replace("\"", ""))
                    pre_close_price = __parse_float(ss[3].replace("\"", ""), pre_clear_price)
                    open_price = __parse_float(ss[5].replace("\"", ""), pre_clear_price)
                    high_price = __parse_float(ss[6].replace("\"", ""), pre_clear_price)
                    low_price = __parse_float(ss[7].replace("\"", ""), pre_clear_price)
                    close_price = __parse_float(ss[8].replace("\"", ""), pre_clear_price)
                    clear_price = float(ss[9].replace("\"", ""))
                    volumn = int(ss[12].replace("\"", ""))
                    money = float(ss[13].replace("\"", ""))
                    position = int(ss[14].replace("\"", ""))
                    data = FutureBarData(time, open_price, high_price, low_price, \
                        close_price, clear_price, pre_close_price, pre_clear_price, volumn, money, position)
                    
                    if instrument not in md_map:
                        md_map[instrument] = []
                    md_map[instrument].append(data)

def __parse_future_bar_1d_dce_2017(datadir, products, md_map):
    path = os.path.join(datadir, "dce/history_md/history_md_2017_%s.csv")
    for product in products:
        if product.exchange != "DCE":
            continue
        if not os.path.exists(path % product.code):
            continue
        wb = xlrd.open_workbook(path % product.code)
        print("parsing 2017 %s" % product.code)
        ws = wb.sheet_by_index(0)
        for row in range(1, ws.nrows):     #skip the first row
            instrument = ws.cell(row, 1).value
            date = ws.cell(row, 2).value
            if not re.match(regex_date, date):
                continue
            time = datetime.datetime.strptime(date, "%Y%m%d")
            pre_close_price = float(ws.cell(row, 3).value)
            pre_clear_price = float(ws.cell(row, 4).value)
            open_price = __parse_float(ws.cell(row, 5).value, pre_clear_price)
            high_price = __parse_float(ws.cell(row, 6).value, pre_clear_price)
            low_price = __parse_float(ws.cell(row, 7).value, pre_clear_price)
            close_price = __parse_float(ws.cell(row, 8).value, pre_clear_price)
            clear_price = float(ws.cell(row, 9).value)
            volumn = int(ws.cell(row, 12).value)
            money = float(ws.cell(row, 13).value)
            position = float(ws.cell(row, 14).value)
            data = FutureBarData(time, open_price, high_price, low_price, \
                close_price, clear_price, pre_close_price, pre_clear_price, volumn, money, position)
            
            if instrument not in md_map:
                md_map[instrument] = []
            md_map[instrument].append(data)

def __parse_future_bar_1d_dce_2018(datadir, products, md_map):
    path = os.path.join(datadir, "dce/history_md/history_md_2018_%s.xlsx")
    for product in products:
        if product.exchange != "DCE":
            continue
        wb = xlrd.open_workbook(path % product.code)
        print("parsing 2018 %s" % product.code)
        ws = wb.sheet_by_index(0)
        for row in range(1, ws.nrows):     #skip the first row
            instrument = ws.cell(row, 2).value
            date = ws.cell(row, 3).value
            if not re.match(regex_date, date):
                continue
            time = datetime.datetime.strptime(date, "%Y%m%d")
            pre_close_price = float(ws.cell(row, 4).value)
            pre_clear_price = float(ws.cell(row, 5).value)
            open_price = __parse_float(ws.cell(row, 6).value, pre_clear_price)
            high_price = __parse_float(ws.cell(row, 7).value, pre_clear_price)
            low_price = __parse_float(ws.cell(row, 8).value, pre_clear_price)
            close_price = __parse_float(ws.cell(row, 9).value, pre_clear_price)
            clear_price = float(ws.cell(row, 10).value)
            volumn = int(ws.cell(row, 13).value)
            money = float(ws.cell(row, 14).value)
            position = float(ws.cell(row, 15).value)
            data = FutureBarData(time, open_price, high_price, low_price, \
                close_price, clear_price, pre_close_price, pre_clear_price, volumn, money, position)
            
            if instrument not in md_map:
                md_map[instrument] = []
            md_map[instrument].append(data)

def init_future_bar_1d_dce(store, datadir):
    products = store.get_all(FutureProduct)
    ins_list = []
    md_map = {}
    __parse_future_bar_1d_dce_zip(datadir, products, md_map)
    __parse_future_bar_1d_dce_2017(datadir, products, md_map)
    __parse_future_bar_1d_dce_2018(datadir, products, md_map)
    for instrument, items in md_map.items():
        items.sort(key=lambda x:x.time)
        store.write_all(items, FutureBarData, ["1d", instrument])

        if instrument[1].isdigit():
            product = instrument[:1]
        else:
            product = instrument[:2]
        ins = FutureInstrument("DCE", product, instrument)
        ins_list.append(ins)
    
    ins_list.sort(key=str)
    store.append_all(ins_list, FutureInstrument)
    store.set_last_update(datetime.datetime.strptime("20190101", "%Y%m%d"), FutureBarData, ["1d", "dce"])

def init_future_bar_1d_czce(store, datadir):
    ins_list = []
    md_map = {}
    path = os.path.join(datadir, "czce/history_md/datahistory%d.zip")
    newpath = os.path.join(datadir, "czce/history_md/unzip/datahistory%d.csv")
    tmpdir = os.path.join(datadir, "czce/history_md/unzip")
    if not os.path.exists(tmpdir):
        os.makedirs(tmpdir)
    for year in range(2010, 2019):
            filename = path % (year)
            newfilename = newpath % (year)
            if not os.path.exists(filename):
                continue
            print("processing %s" % filename)
            zfile = zipfile.ZipFile(filename)
            for fn in zfile.namelist():
                with open(newfilename, 'wb') as output_file:
                    with zfile.open(fn, 'r') as origin_file:
                        shutil.copyfileobj(origin_file, output_file)

            try:
                fp = open(newfilename, "r", encoding="gbk")
                lines = fp.readlines()
            except:
                fp = open(newfilename, "r")
                lines = fp.readlines()

            for line in lines[2:]:
                ss = line.split("|")
                if len(ss) != 16:
                    continue
                date = ss[0].strip()
                time = datetime.datetime.strptime(date, "%Y-%m-%d")
                instrument = ss[1].strip()
                pre_clear_price = float(ss[2].strip().replace(",", ""))
                pre_close_price = pre_clear_price
                open_price = __parse_float(ss[3].strip().replace(",", ""), pre_clear_price)
                high_price = __parse_float(ss[4].strip().replace(",", ""), pre_clear_price)
                low_price = __parse_float(ss[5].strip().replace(",", ""), pre_clear_price)
                close_price = __parse_float(ss[6].strip().replace(",", ""), pre_clear_price)
                clear_price = float(ss[7].strip().replace(",", ""))
                volumn = int(ss[10].strip().replace(",", ""))
                money = float(ss[13].strip().replace(",", ""))
                position = int(ss[11].strip().replace(",", ""))
                data = FutureBarData(time, open_price, high_price, low_price, \
                    close_price, clear_price, pre_close_price, pre_clear_price, volumn, money, position)
                
                if instrument not in md_map:
                    md_map[instrument] = []
                md_map[instrument].append(data)

    for instrument, items in md_map.items():
        items.sort(key=lambda x:x.time)
        store.write_all(items, FutureBarData, ["1d", instrument])

        if instrument[1].isdigit():
            product = instrument[:1]
        else:
            product = instrument[:2]
        ins = FutureInstrument("CZCE", product, instrument)
        ins_list.append(ins)
    
    ins_list.sort(key=str)
    store.append_all(ins_list, FutureInstrument)
    store.set_last_update(datetime.datetime.strptime("20190101", "%Y%m%d"), FutureBarData, ["1d", "czce"])

if __name__ == "__main__":
    from pylon.store.csv import CsvDataStore
    store = CsvDataStore("./", "test")
    init_future_bar_1d_czce(store, "../data")
