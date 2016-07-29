#!/usr/bin/env python
# -*- coding: utf-8 -*-
# creat: 2016-07-25
#

import os
import sae
import web
import model

from wechatInterface import WechatInterface

urls = (
    '/', 'Hello',
    '/weixin', 'WechatInterface',
    '/ck', 'feedback',
)

app_root = os.path.dirname(__file__)
templates_root = os.path.join(app_root, 'templates')
render = web.template.render(templates_root)

class Hello:
    def GET(self):
        return render.text("Hello World！")

class feedback:
    def GET(self):
        fkcon = model.get_fkcontent()
        return render.checkfk(fkcon)

app = web.application(urls, globals()).wsgifunc()

application = sae.create_wsgi_app(app)
