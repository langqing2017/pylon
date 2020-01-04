# -*- coding: utf-8 -*-

"""
Download history md from dce
Created on 2019/12/22
@author: langqing2017
@group : pylon
"""

import urllib.request
from bs4 import BeautifulSoup

def read_product():
    f = open("../../future_product.csv")
    lines = f.readlines()
    f.close()

    product_map = {}
    for line in lines:
        ss = line.split(",")
        if len(ss) < 5:
            continue
        if ss[0] != "DCE":
            continue
        product_code = ss[1].strip()
        product_name = ss[2].strip()
        product_map[product_name] = product_code
    return product_map

def fetch(product_map):
    response = urllib.request.urlopen('http://www.dce.com.cn/dalianshangpin/xqsj/lssj/index.html')
    soup = BeautifulSoup(response.read(), "lxml")
    ul_list = soup.select("ul.cate_sel.clearfix")
    year = 2018
    for ul in ul_list:
        for li in ul.select("li"):
            product_name = li.label.text
            if product_name.endswith("期权"):
                continue
            product_code = product_map[product_name]
            fileurl = li.input["rel"]
            filename = "history_md_%d_%s.%s" % (year, product_code, fileurl.split(".")[1])
            print("fetching %s" % filename)
            response = urllib.request.urlopen("http://www.dce.com.cn%s" % fileurl)
            data = response.read()
            f = open(filename, "wb")
            f.write(data)
            f.close()
            
        year -= 1
        if year < 2010:
            break

if __name__ == "__main__":
    product_map = read_product()
    fetch(product_map)


