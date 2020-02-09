# -*- coding: utf-8 -*-

"""
Stock List Data Fetch
Created on 2020/2/8
@author: langqing2017
@group : pylon
"""

import urllib.request
import datetime
import demjson
from pylon.model.type_convert import *
from pylon.model.stock import StockInstrument, StockBarData

SINA_MD_URL = "http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=%d&num=100&sort=symbol&asc=1&node=%s&symbol=&_s_r_a=page"
MARKETS = {
    "沪市A股": "sh_a",
    "沪市B股": "sh_b",
    "深市A股": "sz_a",
    "深市B股": "sz_b"
}

def fetch_stock_instrument_and_bardata():
    now = datetime.datetime.now()
    instruments = []
    bardata_map = {}
    for market, node in MARKETS.items():
        for i in range(1, 100):
            request = urllib.request.Request(SINA_MD_URL % (i, node), headers={'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'})
            response = urllib.request.urlopen(request)
            s = response.read().decode("gbk")
            dlist = demjson.decode(s)
            if dlist == None or len(dlist) <= 0: 
                break
            print("fetch stock %s: %d" % (market, len(dlist)))

            for data in dlist: 
                if data["symbol"].startswith("sh"):
                    exchange = "SSE"
                elif data["symbol"].startswith("sz"):
                    exchange = "SZE"
                code = data["symbol"][2:]
                instrument_id = "%s.%s" % (exchange, code)
                instrument = StockInstrument(instrument_id, exchange, market, code, data["name"])
                instruments.append(instrument)

                bardata = StockBarData(now, float(data["open"]), float(data["high"]), float(data["low"]), \
                    float(data["trade"]), float(data["settlement"]), data["volume"], data["amount"])
                bardata_map[instrument_id] = bardata
    return instruments, bardata_map

if __name__ == "__main__":
    print(fetch_stock_bardata())
