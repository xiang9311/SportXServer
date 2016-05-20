from django.shortcuts import render
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .dependency import common_pb2, token_pb2, pilot_pb2
from .service import userService

import time

from SportXServer import qiniuUtil, log
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
    common.message = "ERROR.--message from background."
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
    cmdId = 11001
    response_pro = token_pb2.Response11001()
    try:
        response_common = response_pro.common
        data = response_pro.data
        data.qiniuToken = qiniuUtil.getQiniuTokenWithOutKey()
        data.bucketName = qiniuUtil.getDefaultBucketName()
        initCommonResponse(0, 'success', cmdId, 0, response_common)
        return HttpResponse(response_pro.SerializeToString())
    except Exception as error:
        initCommonErrorResponse(cmdId, 101, response_pro.common)
        return HttpResponse(response_pro.SerializeToString())


@csrf_exempt
def getRongToken(request):
    """
    获取新融云token
    解析request
    构造response
    """
    cmdId = 11002
    request_pro = token_pb2.Request11002()
    response_pro = token_pb2.Response11002()
    try:
        log.debug("read success")
        request_pro.MergeFromString(request.read())
    except:
        log.debug("read failed")
        initCommonErrorResponse(cmdId, 101, response_pro.common)
        return HttpResponse(response_pro.SerializeToString())

    request_common = request_pro.common
    request_params = request_pro.params
        #检查common(userid userkey else)

    try:
        userService.userExist(request_common.userid)
    except:
        #未注册用户
        initCommonErrorResponse(cmdId, 101, response__pro.common)
        return HttpResponse(response__pro.SerializeToString())


    #response
    try:

        response_common = response_pro.common
        response_data = response_pro.data
        initCommonResponse(0, 'success', cmdId, 0, response_common)
        response_data.rongyunToken = userService.getRongToken(request_common.userid)
        return HttpResponse(response_pro.SerializeToString())
        
    except:
        log.debug("rongyunToken failed")
        initCommonErrorResponse(cmdId, 101, response_pro.common)
        return HttpResponse(response_pro.SerializeToString())


"""
用户相关
"""


@csrf_exempt
def verifyPhoneCanUse(request):
    cmdId = 10016
    request_pro = pilot_pb2.Request10016()
    response_pro = pilot_pb2.Response10016()
    try:
        request_pro.MergeFromString(request.read())
    except:
        #如果读取异常直接返回一个error
        log.debug('comunications failed')
        initCommonErrorResponse(cmdId, 101, response_pro.common)
        return HttpResponse(response_pro.SerializeToString())

    request_common = request_pro.common       #注册不用检查requestcommon
    request_params = request_pro.params

    try:

        response_common = response_pro.common
        response_data = response_pro.data
        initCommonResponse(0, 'success', cmdId, 0, response_common)

        phone = request_params.phone

        if userService.phoneExist(phone):
            response_data.canUser = False
            log.debug('phone can not use for %s' % phone)
            return HttpResponse(response_pro.SerializeToString())
        else:
            response_data.canUser = True
            log.debug('phone can use for %s' % phone)
            return HttpResponse(response_pro.SerializeToString())

    except Exception as error:
        initCommonErrorResponse(cmdId, 102, response_pro.common)
        return HttpResponse(response_pro.SerializeToString())


@csrf_exempt
def register(request):
    """
    注册
    :param request:
    :return:
    """
    cmdId = 10001
    request_pro = pilot_pb2.Request10001()
    response_pro = pilot_pb2.Response10001()
    try:
        request_pro.MergeFromString(request.read())

    except:
        #如果读取异常直接返回一个error
        log.debug('comunications failed')
        initCommonErrorResponse(cmdId, 101, response_pro.common)
        return HttpResponse(response_pro.SerializeToString())


    request_common = request_pro.common       #注册不用检查requestcommon
    request_params = request_pro.params


    try:
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
        log.error(str(error))
        initCommonErrorResponse(cmdId, 101, response_pro.common)
        return HttpResponse(response_pro.SerializeToString())

@csrf_exempt
def login(request):
    """
    登录只检测com？
    param : requset
    return : success/failes
    """
    cmdId = 10002
    request_pro = pilot_pb2.Request10002()
    response_pro = pilot_pb2.Response10002()
    try:
        request_pro.MergeFromString(request.read())
    except:
        #如果读取异常直接返回一个error
        log.debug('comunications failed')
        initCommonErrorResponse(cmdId, 101, response_pro.common)
        return HttpResponse(response_pro.SerializeToString())


    request_common = request_pro.common
    request_params = request_pro.params

    #构造返回

    try:
        response_common = response_pro.common
        response_data = response_pro.data
        initCommonResponse(0, 'success', cmdId, 0, response_common)

        if  userService.login(request_params.phone, request_params.password, response_data):
            log.info("登录成功")
            return HttpResponse(response_pro.SerializeToString())
        else :
            log.error("登录失败")
            initCommonErrorResponse(cmdId, 1, response_common)
            return HttpResponse(response_pro.SerializeToString())
    except Exception as error:
        log.error(str(error))
        initCommonErrorResponse(cmdId, 101, response_pro.common)
        return HttpResponse(response_pro.SerializeToString())










"""
搜索相关
"""

@csrf_exempt
def searchUser(request):
    cmdId = 11013
    request_pro = pilot_pb2.Request11013()
    response_pro = pilot_pb2.Response11013()
    try:
        request_pro.MergeFromString(request.read())
    except Exception as error:
        #如果读取异常直接返回一个error
        log.error('comunications failed')
        log.error(str(error))
        initCommonErrorResponse(cmdId, 101, response_pro.common)
        return HttpResponse(response_pro.SerializeToString())

    request_common = request_pro.common
    request_params = request_pro.params

    log.info("搜索:数据解析成功" + str(request_params))

    #构造返回

    try:
        response_common = response_pro.common
        response_data = response_pro.data
        initCommonResponse(0, 'success', cmdId, 0, response_common)

        if  userService.searchUser(request_params.keyword, request_params.pageIndex, response_data):
            log.info("搜索成功")
            return HttpResponse(response_pro.SerializeToString())
        else :
            initCommonErrorResponse(cmdId, 1, response_common)
            return HttpResponse(response_pro.SerializeToString())
    except Exception as error:
        log.error(str(error))
        initCommonErrorResponse(cmdId, 103, response_pro.common)
        return HttpResponse(response_pro.SerializeToString())
    pass