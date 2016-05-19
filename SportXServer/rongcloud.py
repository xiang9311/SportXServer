#! /usr/bin/env python
# coding=utf-8
#代码为rongcloud的git上提供设置代码，尚未更改
import os
import json
import unittest
import logging

from Background.dependency.rong import ApiClient

#app_key = ""
#app_secret = ""

#os.environ.setdefault('rongcloud_app_key', app_key)
#os.environ.setdefault('rongcloud_app_secret', app_secret)

logging.basicConfig(level=logging.INFO)

client = ApiClient()

def get_token(self,userid,username,imaginurl):
    result = client.user_get_token(userid,username,imageurl)
    if result[u'code'] == 200 :
        return result[u'token']
