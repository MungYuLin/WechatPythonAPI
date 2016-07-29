#!/usr/bin/env python
# -*- coding: utf-8 -*-
# creat: 2016-07-28
#

import urllib
import urllib2
import json
import model

class CreativeManager:

    def __init__(self):
        self.batchgetMaterialUrl = 'https://api.weixin.qq.com/cgi-bin/material/batchget_material?access_token='
        self.getMaterialUrl = 'https://api.weixin.qq.com/cgi-bin/material/get_material?access_token='

    def getCreativeList(self, stype, offset=0, count=20):
        url = self.batchgetMaterialUrl + model.getAccessToken()
        data = {
            "type": stype, # 图片（image）、视频（video）、语音 （voice）、图文（news）
            "offset": offset, # 偏移位置开始返回
            "count": count # 返回素材的数量
        }
        request = urllib2.Request(
            url = url,
            data = urllib.urlencode(data)
        )
        response = urllib2.urlopen(request)
        result = response.read()
        if result:
            return result['item']
        return None

    def getMaterial(self, media_id):
        url = self.getMaterialUrl + model.getAccessToken()
        data = {
            "media_id": media_id
        }
        request = urllib2.Request(
            url = url,
            data = urllib.urlencode(data)
        )
        response = urllib2.urlopen(request)
        result = response.read()
        if result:
            return result
        return None
