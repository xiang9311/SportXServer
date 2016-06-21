#! /usr/bin/env python
# coding=utf-8
#代码为rongcloud的git上提供设置代码，尚未更改
import os
import json
import unittest
import logging

from Background.dependency.rong import ApiClient

__APP_KEY__ = 'qd46yzrf48y6f'
__APP_SECRET__ = '9I77BwAYh2u'

os.environ.setdefault('rongcloud_app_key', __APP_KEY__)
os.environ.setdefault('rongcloud_app_secret', __APP_SECRET__)

logging.basicConfig(level=logging.INFO)

client = ApiClient()

def get_token(userid,username,imageurl):
    result = client.user_get_token(userid,username,imageurl)
    if result['code'] == 200 :
        return result['token']
