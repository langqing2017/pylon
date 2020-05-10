# -*- coding: utf-8 -*-

"""
Utils for urllib
Created on 2020/1/4
@author: langqing2017
@group : pylon
"""

import urllib.request
import urllib.error

def fetch_url(url, encode="gbk", retry=3, post=None, allow_404=False):
    while retry > 0:
        try:
            if post == None:
                request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'})
            else:
                data = urllib.parse.urlencode(post).encode(encode)
                request = urllib.request.Request(url, method="POST", data=data, headers={'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'})
            response = urllib.request.urlopen(request)
            s = response.read().decode(encode, "replace")
            break
        except Exception as e:
            if type(e) is urllib.error.HTTPError:
                if e.code == 404 and allow_404:
                    return ""
            retry -= 1
            if retry <= 0:
                print("fetch url failed: %s" % url)
                raise e
    return s
