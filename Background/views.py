from django.shortcuts import render
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .dependency import common_pb2, token_pb2, pilot_pb2
from .service import userService

import time

from SportXServer import qiniuUtil
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
    cmdId = 11001
    try:
        response11001 = token_pb2.Response11001()
        response_common = response11001.common
        data = response11001.data
        data.qiniuToken = qiniuUtil.getQiniuTokenWithOutKey()
        initCommonResponse(0, 'success', 10001, 0, response_common)
        return HttpResponse(response11001.SerializeToString())
    except Exception as error:
        response11001 = token_pb2.Response11001()
        initCommonErrorResponse(10001, 101, response11001.common)
        return HttpResponse(response11001.SerializeToString())

@csrf_exempt
def getRongToken(request):
    """
    获取新融云token
    解析request
    构造response
    """
    if DEBUGMODE==True:
        cmdId = 11002
        userid = 1
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
        suserService.login(request_common.userid,request_common.userkey)
    except:
        #未注册用户
        #return HttpResponse("weizhuce")
        pass


    #response
    try:
        respose11002 = token_pb2.Respose11002()
        response_common = response_pro.common
        response_data = response_pro.data
        initCommonResponse(0, 'success', cmdId, 0, response_common)
        response_data.rongyunToken = Service.getRongToken(userid)
        return HttpResponse(response11002.SerializeToString())
        
    except:
        if TRACEMODE == True:
            print(" failed")
        initCommonErrorResponse(cmdId, 101, response10001.common)
        return HttpResponse(response11001.SerializeToString())


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
        if DEBUGMODE == True:
            phone = "18810278575"
            username = 'yxx'
            avatarKey = 'url'
            bucketName = 'sportx'
            password = 'password'
            sex = True

        else:
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
        response_pro = pilot_pb2.Response10001()
        initCommonErrorResponse(cmdId, 101, response10001.common)
        return HttpResponse(response10001.SerializeToString())


def login(request):
    """
    登录只检测com？
    param : requset
    return : success/failes
    """
    request10002 = pilot_pb2.Request10002()
    try:
        request10002.MergeFromString(requset.read())
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
        
    except:
        pass
    #user=userService.login(request_params.phone,request_params.password)
    user = userService.login('18810278575','password', response_data)
    userKey = request_common.userkey
    if  user:
        #DATA
        print('in')
        return HttpResponse(response10002.SerializeToString())
    else :
        initCommonErrorResponse(cmdId, 1, response_common)
        return HttpResponse(response10002.SerializeToString())