#!/usr/bin/env python
# -*- coding: utf-8 -*-
# creat: 2016-07-25
#

import urllib
import urllib2
import re, json
# import requests

class NetMusic:

    def __init__(self):
        self.timeout = 100
        self.header = {
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.8,gl;q=0.6,zh-TW;q=0.4',
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Connection': 'Keep-Alive',
            'Referer': 'http://music.163.com/search/',
            'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
        }

    def search(self, keyword, stype=1, offset=0, total='true', limit=100):
        action = 'http://s.music.163.com/search/get/'
        data = {
            's': keyword.encode('utf-8'),
            'type': stype,
            'offset': offset,
            'total': total,
            'limit': limit
        }
        return self.httpRequest(action, data)

    def songs_detail(self, ids, offset=0):
        tmpids = ids[offset:]
        tmpids = tmpids[0:100]
        tmpids = map(str, tmpids)
        action = 'http://music.163.com/api/song/detail?ids=[' + (',').join(tmpids) + ']'
        try:
            data = self.httpRequest('GET', action)
            return data['songs']
        except:
            return []

    # 有问题，返回是页面，需要返回音乐列表
    def get_playlist(self, playlist_id=None):
        # url = 'http://music.163.com/discover/toplist?id=' + playlist_id
        # response = urllib2.urlopen(url)
        # data = response.read()
        data = [
            [r'http://m2.music.126.net/O04Y-NOmYdmDq1LlLOyBDg==/3416182636066202.mp3', '陈鸿宇-理想三旬', '这首歌从曲来讲，淡淡的吉他弹奏的一曲舒缓虽然重复，但是韵律十足。词填的非常唯美，能将一个唯美的爱情故事娓娓道来，也许每个人都会在青春有一场刻骨铭心的恋爱，可最后却痛心放手，当岁月已去，午后阳光洒在书桌上，暖暖的，一杯咖啡，氲氲的，又抚起那积了灰的吉他，便是爱情温存。'],
            [r'http://m2.music.126.net/iSX7oxJtCbPaXh-qZT6o9w==/3268848069435293.mp3', '陈奕迅-不要说话', '这首歌的低音部分很适合陈奕迅的声线，低低的不间断的流动的旋律，配合叙述感觉的歌词，平静又温暖，副歌部分的旋律上口易记，歌曲整体的旋律性很好，是让人听到第一耳就会爱上的好歌。'],
            [r'http://m2.music.126.net/XTcyeYlhmqtyj7PX4dzRAg==/5994537395163433.mp3', '程璧-给猫夏的你', '民谣音乐人程璧演唱的一首歌曲'],
            [r'http://m2.music.126.net/FFAOyLj7o56Y_q0kUYr9bQ==/3413983604420719.mp3', '李克勤-月半小夜曲', '李克勤代表作之一'],
            [r'http://m2.music.126.net/LpD2YmYAbGmOJ1MA5km7SQ==/2115460371842838.mp3', '李健-陀螺', '这首歌在写人，人和人的冲突，人和世界的冲突，人和自己的冲突，近乎一种黑色有一些绝望，很凝重的作品。'],
            [r'http://m2.music.126.net/j_UJ3vwn8piSUHYfVzqZ-Q==/2750978092703827.mp3', '周笔畅-对嘴', '《对嘴》是周笔畅演唱的一首歌曲，歌曲由陈小霞作曲，姚若龙作词，歌曲收录在周笔畅2011新专辑《黑择明》中'],
            [r'http://m2.music.126.net/ygWA7r7xgAw1Ztb_dABCpg==/1378787594453475.mp3', '陈奕迅-在这个世界相遇', '动画电影《大鱼海棠》的主题曲，这首歌由窦鹏作曲，田晓鹏作词，陈奕迅演唱。']
        ]
        return data

    def httpRequest(self, action, query=None):
        request = urllib2.Request(
            url = action,
            data = urllib.urlencode(query),
            headers = self.header
        )
        try:
            response = urllib2.urlopen(request)
            the_page = response.read()
            connection = json.loads(the_page)
            return connection
        except urllib2.URLError, e:
            return e.code
