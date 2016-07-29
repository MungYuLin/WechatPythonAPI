#!/usr/bin/env python
# -*- coding: utf-8 -*-
# creat: 2016-07-28
#

import urllib, urllib2
import json, time, random
import os, web
import netMusic, doubanBook, model
import creativeManager
import lxml
from lxml import etree

class WechatCallbackAPI:

    def __init__(self):
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root, 'templates')
        self.render = web.template.render(self.templates_root)
        self.musicSearch = netMusic.NetMusic()
        self.bookSearch = doubanBook.DoubanBook()
        self.creative = creativeManager.CreativeManager()

    def getCreative(self):
        # 获取素材信息
        result = self.creative.getCreativeList(stype='news', offset=0, count=1)
        return result

    def receiveEvent(self, xml, fromUser, toUser, createTime):
        mscontent = xml.find("Event").text.lower()
        if mscontent == "subscribe":
            replayText = u'欢迎关注Mandag，可回复“help”查看操作指令。'
            return self.render.reply_text(fromUser, toUser, createTime, replayText)
        elif mscontent == "unsubscribe":
            return self.render.reply_text(fromUser, toUser, createTime, u'88')
        elif mscontent == "click":
            mskey = xml.find("EventKey").text
            if mskey == "menu_service":
                return self.render.reply_text(fromUser, toUser, createTime, u'服务')
            elif mskey == "menu_words":
                return self.render.reply_text(fromUser, toUser, createTime, u'作品')
            elif mskey == "menu_about":
                return self.render.reply_text(fromUser, toUser, createTime, u'关于')
            elif mskey == "menu_location":
                return self.render.reply_text(fromUser, toUser, createTime, u'已收到服务地址')
            elif mskey == "menu_help":
                replayText = u'1. 输入 book 要查询的书名 返回豆瓣图书中结果\n2. 输入music随机来首音乐听，建议在wifi下听\n3. 输入 m 要查询的歌名 返回网易云音乐中结果\n4. 输入ly 内容 留言反馈意见\n5. 输入clear清除查询记录'
                return self.render.reply_text(fromUser, toUser, createTime, replayText)
            else:
                return self.render.reply_text(fromUser, toUser, createTime, mskey)

    def receiveText(self, xml, fromUser, toUser, createTime):
        content = xml.find("Content").text.lower()
        if content == 'music':
            musiclist = self.musicSearch.get_playlist('19723756')
            music = random.choice(musiclist)
            musicurl = music[0]
            musictitle = music[1]
            musicdesc = music[2]
            return self.render.reply_music(fromUser, toUser, createTime, musictitle, musicdesc, musicurl)

        elif content.startswith('m '):
            keyword = content.replace('m ','')
            if keyword is None:
                return self.render.reply_text(fromUser, toUser, createTime, u'请输入关键字查询！')
            else:
                musics = self.musicSearch.search(keyword, limit=1)
                if not musics['result']:
                    return self.render.reply_text(fromUser, toUser, createTime, u'未找到该歌曲！')
                try:
                    musictitle = '%s-%s' % (musics['result']['songs'][0]['artists'][0]['name'], musics['result']['songs'][0]['name'])
                    musicdesc = u'来自网易云音乐'
                    musicurl = musics['result']['songs'][0]['audio']
                    return self.render.reply_music(fromUser, toUser, createTime, musictitle, musicdesc, musicurl)
                except IndexError:
                    return self.render.reply_text(fromUser, toUser, createTime, u'未找到该歌曲！')

        elif content.startswith('book '):
            keyword = content.replace('book ','')
            if keyword is None:
                return self.render.reply_text(fromUser, toUser, createTime, u'请输入关键字查询！')
            else:
                book = self.bookSearch.search(keyword)
                return self.render.reply_text(fromUser, toUser, createTime, book)

        elif content.startswith('ly '):
            fktime = time.strftime('%Y-%m-%d %H:%M',time.localtime())
            model.addfk(fromUser, fktime, content[3:].encode('utf-8'))
            return self.render.reply_text(fromUser, toUser, createTime, u'感谢您的反馈！')

        elif content == 'clear':
            return self.render.reply_text(fromUser, toUser, createTime, u'哦，还没写呢~')

        elif content == 'help':
            replayText = u'1. 输入 book 要查询的书名 返回豆瓣图书中结果\n2. 输入music随机来首音乐听，建议在wifi下听\n3. 输入 m 要查询的歌名 返回网易云音乐中结果\n4. 输入ly 内容 留言反馈意见\n5. 输入clear清除查询记录'
            return self.render.reply_text(fromUser, toUser, createTime, replayText)

        else:
            replayText = u'不好意思，我不知道您的意思是什么！'
            return self.render.reply_text(fromUser, toUser, createTime, replayText)

    def responseMsg(self, xml):
        msgType = xml.find("MsgType").text
        fromUser = xml.find("FromUserName").text
        toUser = xml.find("ToUserName").text
        createTime = int(time.time())

        if msgType == "event":
            return self.receiveEvent(xml, fromUser, toUser, createTime)

        if msgType == 'text':
            return self.receiveText(xml, fromUser, toUser, createTime)
