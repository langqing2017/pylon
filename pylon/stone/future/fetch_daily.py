# -*- coding: utf-8 -*-

"""
Future Daily Data Fetch
Created on 2020/1/4
@author: langqing2017
@group : pylon
"""

import urllib.request
import re
import datetime
import json
from pylon.model.future import FutureBarData

regex_code = "^[a-zA-Z0-9]{5,6}$"
regex_delivery_month = "^\d{4}$"

def __parse_float(str, value):
    if str == "" or str == "0":
        return value
    return float(str)

def __parse_int(str):
    if str == "":
        return 0
    return int(str)

def fetch_future_daily_shfe(date, product_map):
    url = "http://www.shfe.com.cn/data/dailydata/kx/kx%s.dat" % date.strftime("%Y%m%d")
    request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'})
    response = urllib.request.urlopen(request)
    txt = response.read().decode()
    data = json.loads(txt)
    md_map = {}
    for item in data["o_curinstrument"]:
        product = item["PRODUCTNAME"].strip()
        if product not in product_map:
            continue
        if not re.match(regex_delivery_month, item["DELIVERYMONTH"]):
            continue
        instrument = "%s%s" % (product_map[product], item["DELIVERYMONTH"])
        pre_clear_price = float(item["PRESETTLEMENTPRICE"])
        pre_close_price = pre_clear_price
        open_price = __parse_float(item["OPENPRICE"], pre_clear_price)
        high_price = __parse_float(item["HIGHESTPRICE"], pre_clear_price)
        low_price = __parse_float(item["LOWESTPRICE"], pre_clear_price)
        close_price = __parse_float(item["CLOSEPRICE"], pre_clear_price)
        clear_price = __parse_float(item["SETTLEMENTPRICE"], pre_clear_price)
        volumn = __parse_int(item["VOLUME"])
        money = 0.0
        position = int(item["OPENINTEREST"])
        data = FutureBarData(date, open_price, high_price, low_price, \
            close_price, clear_price, pre_close_price, pre_clear_price, volumn, money, position)
        md_map[instrument] = data
    return md_map

def fetch_future_daily_dce(date, product_map):
    url = "http://www.dce.com.cn/publicweb/quotesdata/exportDayQuotesChData.html"
    data = {
            "dayQuotes.variety": "all",
            "dayQuotes.trade_type": "0",
            "year": date.year,
            "month": date.month-1,
            "day": date.day,
            "exportFlag": "txt"
        }
    post = urllib.parse.urlencode(data).encode('utf-8')
    request = urllib.request.Request(url, data=post, method="POST", headers={'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'})
    response = urllib.request.urlopen(request)
    txt = response.read().decode()
    md_map = {}
    for line in txt.split("\n"):
        line = line.strip()
        ss = [s.strip() for s in line.split("\t") if s != ""]
        if len(ss) != 14:
            continue
        product = ss[0]
        if product not in product_map:
            continue
        instrument = "%s%s" % (product_map[product], ss[1])
        pre_clear_price = float(ss[6].strip().replace(",", ""))
        pre_close_price = pre_clear_price
        open_price = __parse_float(ss[2].strip().replace(",", ""), pre_clear_price)
        high_price = __parse_float(ss[3].strip().replace(",", ""), pre_clear_price)
        low_price = __parse_float(ss[4].strip().replace(",", ""), pre_clear_price)
        close_price = __parse_float(ss[5].strip().replace(",", ""), pre_clear_price)
        clear_price = float(ss[7].strip().replace(",", ""))
        volumn = int(ss[10].strip().replace(",", ""))
        money = float(ss[13].strip().replace(",", ""))
        position = int(ss[11].strip().replace(",", ""))
        data = FutureBarData(date, open_price, high_price, low_price, \
            close_price, clear_price, pre_close_price, pre_clear_price, volumn, money, position)
        md_map[instrument] = data
    return md_map

def fetch_future_daily_czce(date):
    url = "http://www.czce.com.cn/cn/DFSStaticFiles/Future/%s/%s/FutureDataDaily.txt" \
                % (date.strftime("%Y"), date.strftime("%Y%m%d"))
    request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'})
    response = urllib.request.urlopen(request)
    txt = response.read().decode()
    md_map = {}
    for line in txt.split("\n"):
        line = line.strip()
        ss = line.split("|")
        if len(ss) != 14:
            continue
        if not re.match(regex_code, ss[0].strip()):
            continue
        instrument = ss[0].strip()
        pre_clear_price = float(ss[1].strip().replace(",", ""))
        pre_close_price = pre_clear_price
        open_price = __parse_float(ss[2].strip().replace(",", ""), pre_clear_price)
        high_price = __parse_float(ss[3].strip().replace(",", ""), pre_clear_price)
        low_price = __parse_float(ss[4].strip().replace(",", ""), pre_clear_price)
        close_price = __parse_float(ss[5].strip().replace(",", ""), pre_clear_price)
        clear_price = float(ss[6].strip().replace(",", ""))
        volumn = int(ss[9].strip().replace(",", ""))
        money = float(ss[12].strip().replace(",", ""))
        position = int(ss[10].strip().replace(",", ""))
        data = FutureBarData(date, open_price, high_price, low_price, \
            close_price, clear_price, pre_close_price, pre_clear_price, volumn, money, position)
        md_map[instrument] = data
    return md_map

if __name__ == "__main__":
    # print(fetch_future_daily_czce(datetime.datetime.strptime("20191223", "%Y%m%d")))
    # print(fetch_future_daily_dce(datetime.datetime.strptime("20200103", "%Y%m%d"), {"豆一": "a"}))
    print(fetch_future_daily_shfe(datetime.datetime.strptime("20191223", "%Y%m%d"), {"镍": "ni"}))
