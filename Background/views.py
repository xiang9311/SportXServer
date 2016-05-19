from django.shortcuts import render
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .dependency import common_pb2, token_pb2, pilot_pb2
from .service import userService

import time

from SportXServer import qiniuUtil, log
# Create your views here.
TRACEMODE = True
DEBUGMODE = True

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
    try:
        response11001 = token_pb2.Response11001()
        response_common = response11001.common
        data = response11001.data
        data.qiniuToken = qiniuUtil.getQiniuTokenWithOutKey()
        data.bucketName = qiniuUtil.getDefaultBucketName()
        initCommonResponse(0, 'success', cmdId, 0, response_common)
        return HttpResponse(response11001.SerializeToString())
    except Exception as error:
        response11001 = token_pb2.Response11001()
        initCommonErrorResponse(cmdId, 101, response11001.common)
        return HttpResponse(response11001.SerializeToString())


@csrf_exempt
def getRongToken(request):
    """
    获取新融云token
    解析request
    构造response
    """
    cmdId = 11002
    request_pro = token_pb2.Request11002()
    try:
        if TRACEMODE == True:
            print(request_pro.MergeFromString(request.read()))
        request_pro.MergeFromString(request.read())
    except:
        if TRACEMODE == True:
            print("read failed")
        else:
            pass
    request_common = request_pro.common
    request_params = request_pro.params
        #检查common(userid userkey else)
    try:
        userService.login(request_common.userid,request_common.userkey)
    except:
        #未注册用户
        #return HttpResponse("weizhuce")
        pass


    #response
    try:
        respose11002 = token_pb2.Response11002()
        response_common = respose11002.common
        response_data = respose11002.data
        initCommonResponse(0, 'success', cmdId, 0, response_common)
        response_data.rongyunToken = userService.getRongToken(request_common.userid)
        return HttpResponse(respose11002.SerializeToString())
        
    except:
        if TRACEMODE == True:
            print(" failed")
        initCommonErrorResponse(cmdId, 101, respose11002.common)
        return HttpResponse(respose11002.SerializeToString())


"""
用户相关
"""
@csrf_exempt
def verifyPhoneCanUse(request):
    cmdId = 10016
    request_pro = pilot_pb2.Request10016()
    try:
        request_pro.MergeFromString(request.read())
    except:
        pass

    request_common = request_pro.common       #注册不用检查requestcommon
    request_params = request_pro.params

    try:
        response_pro = pilot_pb2.Response10016()
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
        response_pro = pilot_pb2.Response10016()
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
    try:
        request_pro.MergeFromString(request.read())

    except:
        if TRACEMODE == True:
            print("register read failed")
        else:
            pass

    request_common = request_pro.common       #注册不用检查requestcommon
    request_params = request_pro.params


    try:
        response10001 = pilot_pb2.Response10001()
        response_common = response10001.common
        response_data = response10001.data
        initCommonResponse(0, 'success', cmdId, 0, response_common)
        #不会写request那边的构造，
        phone = request_params.phone
        username = request_params.username
        avatarKey = request_params.avatarKey
        bucketName = request_params.bucketName
        password = request_params.password
        sex = request_params.sex
        if TRACEMODE == True:
            print("register read success")

        if userService.register(phone, username, avatarKey, bucketName, password, sex, response_data):
            if TRACEMODE == True:
                print("register save success")
            return HttpResponse(response10001.SerializeToString())
        else:
            initCommonErrorResponse(cmdId, 1, response_common)
            return HttpResponse(response10001.SerializeToString())

    except Exception as error:
        log.error(str(error))
        response_pro = pilot_pb2.Response10001()
        initCommonErrorResponse(cmdId, 101, response10001.common)
        return HttpResponse(response10001.SerializeToString())

@csrf_exempt
def login(request):
    """
    登录只检测com？
    param : requset
    return : success/failes
    """
    cmdId = 10002
    request10002 = pilot_pb2.Request10002()
    try:
        request10002.MergeFromString(request.read())
    except :
        #读取失败
        if TRACEMODE == True:
            print("register read failed")
        else:
            pass
    request_common = request10002.common
    request_params = request10002.params
    #构造返回
    try:
        response10002 = pilot_pb2.Response10002()
        response_common = response10002.common
        response_data = response10002.data
        initCommonResponse(0, 'success', cmdId, 0, response_common)

        if  userService.login(request_params.phone, request_params.password, response_data):
            log.info("登录成功")
            return HttpResponse(response10002.SerializeToString())
        else :
            log.error("登录失败")
            initCommonErrorResponse(cmdId, 1, response_common)
            return HttpResponse(response10002.SerializeToString())
    except Exception as error:
        log.error(str(error))
        response10002 = pilot_pb2.Response10002()
        initCommonErrorResponse(cmdId, 101, response10002.common)
        return HttpResponse(response10002.SerializeToString())

