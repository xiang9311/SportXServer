from django.shortcuts import render
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .dependency import common_pb2, token_pb2, pilot_pb2
from .service import userService

import time

from SportXServer import qiniuUtil
# Create your views here.

def test(request):
    return HttpResponse('ok')

def initCommonResponse(code, message, cmdid, userid, common):
    """
    根据字段构造返回的common
    :param code:
    :param message:
    :param cmdid:
    :param userid:
    :param common:
    :return:
    """
    common.code = code
    common.message = message
    common.cmdid = cmdid
    common.timestamp = int(time.time() * 1000)
    common.userid = userid

def initCommonErrorResponse(cmdid, userid, common):
    """
    根据字段构造返回的common
    :param cmdid:
    :param userid:
    :param common:
    :return:
    """
    common.code = 100
    common.message = "You have found an ERROR.--message from background."
    common.cmdid = cmdid
    common.timestamp = int(time.time() * 1000)
    common.userid = userid



@csrf_exempt
def getQiniuToken(request):
    """
    获取七牛token， 不用解析request，直接构造返回数据即可
    :param request:
    :return:
    """
    try:
        response10001 = token_pb2.Response11001()
        response_common = response10001.common
        data = response10001.data
        initCommonResponse(0, 'success', 10001, 0, response_common)

        data.qiniuToken = qiniuUtil.getQiniuTokenWithOutKey()

        return HttpResponse(response10001.SerializeToString())
    except Exception as error:
        response10001 = token_pb2.Response11001()
        initCommonErrorResponse(10001, 101, response10001.common)
        return HttpResponse(response10001.SerializeToString())

"""
用户相关
"""
@csrf_exempt
def register(request):
    """
    注册
    :param request:
    :return:
    """
    cmdId = 10001
    request_pro = pilot_pb2.Request10001()
    try:
        request_pro.MergeFromString(request.read())
    except:

        pass

    request_common = request_pro.common       #注册不用检查requestcommon
    request_params = request_pro.params

    try:
        response_pro = pilot_pb2.Response10001()
        response_common = response_pro.common
        response_data = response_pro.data
        initCommonResponse(0, 'success', cmdId, 0, response_common)

        phone = request_params.phone
        username = request_params.username
        avatarKey = request_params.avatarKey
        bucketName = request_params.bucketName
        password = request_params.password
        sex = request_params.sex

        if userService.register(phone, username, avatarKey, bucketName, password, sex, response_data):
            return HttpResponse(response_pro.SerializeToString())
        else:
            initCommonErrorResponse(cmdId, 1, response_common)
            return HttpResponse(response_pro.SerializeToString())

    except Exception as error:
        response_pro = pilot_pb2.Response10001()
        initCommonErrorResponse(cmdId, 101, response_pro.common)
        return HttpResponse(response_pro.SerializeToString())

