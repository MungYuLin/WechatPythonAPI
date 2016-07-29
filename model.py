#!/usr/bin/env python
# -*- coding: utf-8 -*-
# creat: 2016-07-27
#

import web
import web.db
import sae.const
import time

# 配置信息 测试公众号
config =  {
    'token': 'gkKV6MjP8YqoYp',
    'appid': 'wx0bab38fd70624c47',
    'appsecret': '011a34ba1b8db33590eef6882c413972',
    'encoding_aes_key': '',
    'access_token': '',
    'token_time': ''
}

# 获取 Access Token
def getAccessToken():
    if config['token_time'] < time.time():
        accessUrl = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (conf['appid'], conf['appsecret'])
        f = urllib2.urlopen(accessUrl)
        accessT = f.read().decode("utf-8")
        jsonT = json.loads(accessT)
        config['access_token'] = jsonT["access_token"]
        config['token_time'] = int(time.time()) + 7000
    return config['access_token']

# 数据库连接
db = web.database(
    dbn = 'mysql',
    host = sae.const.MYSQL_HOST, # 主库域名（可读写）
    port = int(sae.const.MYSQL_PORT), # 端口
    user = sae.const.MYSQL_USER, # 用户名
    passwd = sae.const.MYSQL_PASS, # 密码
    db = sae.const.MYSQL_DB # 数据库名
)

# 新增留言
def addfk(username, fktime, fkcontent):
    return db.insert('fk', user=username, time=fktime, fk_content=fkcontent)

# 获取留言
def get_fkcontent():
    return db.select('fk', order='id')
