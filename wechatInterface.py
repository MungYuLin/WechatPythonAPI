#!/usr/bin/env python
# -*- coding: utf-8 -*-
# creat: 2016-07-25
#

import hashlib
import web
import lxml
import wechatCallbackAPI
import menuManager, model
from lxml import etree

class WechatInterface:

    def __init__(self):
        conf = model.config
        self.token = conf['token']
        self.wechatCallback = wechatCallbackAPI.WechatCallbackAPI()

        wx = menuManager.MenuManager()
        accessToken = model.getAccessToken()
        wx.createMenu(accessToken)

    def GET(self):
        # 获取输入参数
        data = web.input()
        signature = data.signature
        timestamp = data.timestamp
        nonce = data.nonce
        echostr = data.echostr

        # 字典序排序
        list = [self.token, timestamp, nonce]
        list.sort()
        sha1 = hashlib.sha1()
        map(sha1.update,list)
        hashcode = sha1.hexdigest()
        # sha1加密算法

        # 如果是来自微信的请求，则回复echostr
        if hashcode == signature:
            return echostr
        else:
            return None

    def POST(self):
        str_xml = web.data() # 获得post来的数据
        xml = etree.fromstring(str_xml) # 进行XML解析
        return self.wechatCallback.responseMsg(xml)
