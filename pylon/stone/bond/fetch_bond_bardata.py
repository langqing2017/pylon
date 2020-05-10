# -*- coding: utf-8 -*-

"""
Bond Bar Data Fetch
Created on 2020/2/8
@author: langqing2017
@group : pylon
"""

import datetime
import demjson
from pylon.tools.urllib_utils import *
from pylon.model.type_convert import *
from pylon.model.bond import BondInstrument, BondBarData

SINA_BOND_MD_URL = "http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeDataSimple?page=%d&num=100&sort=symbol&asc=1&node=hs_z&_s_r_a=page"
SINA_CB_MD_URL = "http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeDataSimple?page=%d&num=100&sort=symbol&asc=1&node=hskzz_z&_s_r_a=page"
CATEGORY_MAP = {
    "债券": SINA_BOND_MD_URL,
    "可转债": SINA_CB_MD_URL
}

def fetch_bond_instrument_and_bardata():
    now = datetime.datetime.now()
    instruments = []
    bardata_map = {}
    for category, url in CATEGORY_MAP.items():
        for i in range(1, 100):
            s = fetch_url(url % i)
            dlist = demjson.decode(s)
            if dlist == None or len(dlist) <= 0: 
                break
            print("fetch bond md %s: %d" % (category, len(dlist)))

            for data in dlist: 
                if data["symbol"].startswith("sh"):
                    exchange = "SSE"
                elif data["symbol"].startswith("sz"):
                    exchange = "SZE"
                code = data["symbol"][2:]
                instrument_id = "%s.%s" % (exchange, code)
                instrument = BondInstrument(instrument_id, exchange, category, code, data["name"])
                instruments.append(instrument)

                md = BondBarData(now, float(data["open"]), float(data["high"]), float(data["low"]), \
                    float(data["trade"]), float(data["settlement"]), data["volume"], data["amount"])
                bardata_map[instrument_id] = md
    return instruments, bardata_map

if __name__ == "__main__":
    print(fetch_bond_instrument_and_bardata())
