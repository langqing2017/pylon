# -*- coding: utf-8 -*-

"""
Fund Net Value Data Fetch
Created on 2020/2/8
@author: langqing2017
@group : pylon
"""

import datetime
import demjson
from pylon.tools.urllib_utils import *
from pylon.model.type_convert import *
from pylon.model.fund import FundInstrument, FundNetValue

SINA_CF_NV_URL = "http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeDataSimple?page=%d&num=100&sort=symbol&asc=1&node=close_fund&_s_r_a=page"
SINA_OF_NV_URL = "http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getFundNetData?page=%d&num=100&sort=symbol&asc=1&node=open_fund&_s_r_a=page"
SINA_ETF_NV_URL = "http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getFundNetData?page=%d&num=100&sort=symbol&asc=1&node=etf_jz_fund&_s_r_a=page"
SINA_MF_NV_URL = "http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getFundNetData?page=%d&num=100&sort=symbol&asc=1&node=money_fund&_s_r_a=page"
CATEGORY_MAP = {
    "封闭式基金": SINA_CF_NV_URL,
    "开放式基金": SINA_OF_NV_URL,
    "ETF基金": SINA_ETF_NV_URL,
    "货币基金": SINA_MF_NV_URL,
}

def fetch_fund_instrument_and_nv():
    instruments = []
    nvdata_map = {}
    for category, url in CATEGORY_MAP.items():
        for i in range(1, 100):
            s = fetch_url(url % i)
            dlist = demjson.decode(s)
            if dlist == None or len(dlist) <= 0: 
                break
            print("fetch fund %s: %d" % (category, len(dlist)))

            for data in dlist: 
                if data["symbol"].startswith("sh"):
                    exchange = "SSE"
                    code = data["symbol"][2:]
                elif data["symbol"].startswith("sz"):
                    exchange = "SZE"
                    code = data["symbol"][2:]
                elif category == "开放式基金":
                    exchange = "OF"
                    code = data["symbol"]
                elif data["symbol"].startswith("51"):
                    exchange = "SSE"
                    code = data["symbol"]
                elif data["symbol"].startswith("15"):
                    exchange = "SZE"
                    code = data["symbol"]
                instrument_id = "%s.%s" % (exchange, code)
                instrument = FundInstrument(instrument_id, exchange, category, code, data["name"])
                instruments.append(instrument)

                if category == "开放式基金" or category == "ETF基金":
                    if data["date"] != "0000-00-00":
                        nv = FundNetValue(string_to_date(data["date"]), float(data["dwjz"]))
                        nvdata_map[instrument_id] = nv
    return instruments, nvdata_map

if __name__ == "__main__":
    print(fetch_fund_instrument_and_nv())
