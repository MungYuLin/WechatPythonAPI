#!/usr/bin/env python
# -*- coding: utf-8 -*-
# creat: 2016-07-27
#

import urllib
import urllib2
import re

class DoubanBook:
    def __init__(self):
        self.timeout = 100
        self.header = {
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
            'Connection': 'Keep-Alive',
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'https://book.douban.com/',
            'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
        }

    def get_book(self, packet):
        result = ''
    	tmp = re.search(r'<html lang(.*) book-new-nav">',packet)
    	if tmp is not None:
    		result += "图书信息如下："
    		title = re.search(r'<title>(.*)\(豆瓣\)</title>', packet)
    		result += '\n书名：' + title.group(1).strip()
    		author = re.search(r'<span class="pl"> 作者</span>.*?<a class="" href=.*?>(.*?)</a>', packet, re.S)
    		if author:
    			result += '\n作者：' + author.group(1).strip()
    		cbs = re.search(r'<span class="pl">出版社:</span>(.*)<br/>', packet)
    		if cbs:
    			result += '\n出版社：' + cbs.group(1).strip()
    		price = re.search(r'<span class="pl">定价:</span>(.*)<br/>', packet)
    		result += '\n定价：' + price.group(1).strip()
    	else:
    		result += "未找到该图书！"
        return result

    def search(self, keyword):
        action = 'https://book.douban.com/subject_search'
        data = {
            'search_text': keyword.encode('utf-8'),
            'cat': '1001'
        }
        return self.httpRequest(action, data)


    def httpRequest(self, action, query=None):
        request = urllib2.Request(
            url = action,
            data = urllib.urlencode(query),
            headers = self.header
        )
        try:
            response = urllib2.urlopen(request)
            content = response.read()
            links = re.findall(r'href="https://book.douban.com/subject/(\d*)/', content)
            links = sorted(set(links), key = links.index)

            if len(links):
                url = 'http://book.douban.com/subject/' + links[0]
                response1 = urllib2.urlopen(url)
                content1 = response1.read()
                return self.get_book(content1)
            else:
                return "未找到该图书！"

        except urllib2.URLError, e:
            return e.code
