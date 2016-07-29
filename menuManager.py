#!/usr/bin/env python
# -*- coding: utf-8 -*-
# creat: 2016-07-27
#

import urllib
import urllib2
import json
import model

class MenuManager:

    def __init__(self):
        self.delMenuUrl = "https://api.weixin.qq.com/cgi-bin/menu/delete?access_token="
        self.createUrl = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token="
        self.getMenuUrl = "https://api.weixin.qq.com/cgi-bin/menu/get?access_token="

    def delMenu(self, accessToken):
        html = urllib2.urlopen(self.delMenuUrl + accessToken)
        result = json.loads(html.read().decode("utf-8"))
        return result["errcode"]

    def createMenu(self, accessToken):
        menu = {
            "button": [
            {
                "name": "服务",
                "sub_button": [
                    {
                        "type": "click",
                        "name": "全景",
                        "key": "menu_panoramic"
                    }
                ]
            }, {
                "type": "view_limited",
                "name": "作品",
                "media_id": "media_words"
            }, {
                "name": "更多",
                "sub_button": [
                    {
                        "type": "view_limited",
                        "name": "关于",
                        "media_id": "media_about"
                    }, {
                        "type": "location_select",
                        "name": "发送服务位置",
                        "key": "menu_location"
                    }, {
                        "type": "click",
                        "name": "帮助",
                        "key": "menu_help"
                    }
                ]
            }]
        }
        request = urllib2.Request(self.createUrl + accessToken)
        request.add_header('Content-Type', 'application/json')
        request.add_header('encoding', 'utf-8')
        response = urllib2.urlopen(request, json.dumps(menu, ensure_ascii=False))
        content = response.read()
        result = json.loads(content.decode("utf-8"))
        return result["errcode"]

    def getMenu(self, accessToken):
        html = urllib2.urlopen(self.getMenuUrl + accessToken)
        return html.read().decode("utf-8")
