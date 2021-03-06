from django.shortcuts import render
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .dependency import common_pb2, token_pb2, pilot_pb2
from .service import userService
from .gyms import read_club

import time

from SportXServer import qiniuUtil, log
# Create your views here.

def test(request):
    return HttpResponse('ok')

def createGyms(request):
    clubs = read_club.read_club_from_file()
    from .models import TblBriefGym, TblGyminfo
    from SportXServer import timeUtil
    index = 0
    for club in clubs:
        tblBriefGym = TblBriefGym()
        tblBriefGym.gymAvatar = club.cover
        tblBriefGym.createTime = timeUtil.getDatabaseTimeNow()
        tblBriefGym.gymIntro = club.club_intro
        tblBriefGym.gymName = club.name
        tblBriefGym.latitude = club.latitude
        tblBriefGym.longitude = club.longitude
        tblBriefGym.meituan_price = club.price * club.discount
        tblBriefGym.place = club.location
        tblBriefGym.price = club.price
        tblBriefGym.save()

        i = 0
        for image in club.images:
            i += 1
            tblGyminfo = TblGyminfo()
            tblGyminfo.gym = tblBriefGym
            tblGyminfo.createTime = timeUtil.getDatabaseTimeNow()
            tblGyminfo.image = image
            tblGyminfo.imageOrder = i
            tblGyminfo.save()

        print('已经存储 %d 个gym' % index)
        index += 1
        pass

    return HttpResponse("ok")
    pass


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
        log.info("read success")
        request_pro.MergeFromString(request.read())
    except:
        log.info("read failed")
        initCommonErrorResponse(cmdId, 101, response_pro.common)
        return HttpResponse(response_pro.SerializeToString())

    request_common = request_pro.common
    request_params = request_pro.params

    try:
        userService.userExist(request_common.userid,request_common.userkey)
    except:
        #未注册用户
        log.info("unregister")
        initCommonErrorResponse(cmdId, 101, response_pro.common)
        return HttpResponse(response_pro.SerializeToString())

    #response
    try:
        response_common = response_pro.common
        response_data = response_pro.data
        initCommonResponse(0, 'success', cmdId, 0, response_common)
        response_data.rongyunToken = userService.getRongToken(request_common.userid)
        return HttpResponse(response_pro.SerializeToString())
    except Exception as e:
        log.info("rongyunToken failed:" + str(e))
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
    userId = request_common.userid
    log.info("%d:%d,%s" % (cmdId,userId,str(request_params)))

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
    userId = request_common.userid
    log.info("%d:%d,%s" % (cmdId,userId,str(request_params)))
    userId = request_common.userid
    log.info("%d:%d,%s" % (cmdId,userId,str(request_params)))
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

@csrf_exempt
def updateMyInfo(request):
    cmdId = 10004
    request_pro = pilot_pb2.Request10004()
    response_pro = pilot_pb2.Response10004()
    try:
        request_pro.MergeFromString(request.read())
    except:
        #如果读取异常直接返回一个error
        log.debug('comunications failed')
        initCommonErrorResponse(cmdId, 101, response_pro.common)
        return HttpResponse(response_pro.SerializeToString())

    log.info(str(request_pro))

    request_common = request_pro.common
    request_params = request_pro.params
    userId = request_common.userid
    log.info("%d:%d,%s" % (cmdId,userId,str(request_params)))
    #用户检验
    try:
        userService.userExist(request_common.userid,request_common.userkey)
    except:
        #未注册用户
        initCommonErrorResponse(cmdId, 101, response_pro.common)
        return HttpResponse(response_pro.SerializeToString())
    #构造返回

    try:
        response_common = response_pro.common
        response_data = response_pro.data
        initCommonResponse(0, 'success', cmdId, 0, response_common)

        if userService.updateUser(
                request_common.userid
                , request_params.userName
                , request_params.avatarKey
                , request_params.bucketName
                , request_params.sex
                , request_params.sexChanged
                , request_params.sign
                , request_params.phone
                , response_data):
            return HttpResponse(response_pro.SerializeToString())
        else :
            initCommonErrorResponse(cmdId, 1, response_common)
            return HttpResponse(response_pro.SerializeToString())
    except Exception as error:
        log.error(str(error))
        initCommonErrorResponse(cmdId, 101, response_pro.common)
        return HttpResponse(response_pro.SerializeToString())

@csrf_exempt
def guanzhuUser(request):
    cmdId = 10011
    request_pro = pilot_pb2.Request10011()
    response_pro = pilot_pb2.Response10011()
    try:
        request_pro.MergeFromString(request.read())
    except:
        #如果读取异常直接返回一个error
        log.debug('comunications failed')
        initCommonErrorResponse(cmdId, 101, response_pro.common)
        return HttpResponse(response_pro.SerializeToString())


    request_common = request_pro.common
    request_params = request_pro.params
    userId = request_common.userid
    log.info("%d:%d,%s" % (cmdId,userId,str(request_params)))
     #用户检验
    try:
        userService.userExist(request_common.userid,request_common.userkey)
    except:
        #未注册用户
        initCommonErrorResponse(cmdId, 101, response_pro.common)
        return HttpResponse(response_pro.SerializeToString())
    #构造返回

    try:
        response_common = response_pro.common
        response_data = response_pro.data
        initCommonResponse(0, 'success', cmdId, 0, response_common)

        fromUser = request_common.userid
        toUser = request_params.toUserId
        follow = request_params.isFollow

        if userService.guanzhuUser(fromUser, toUser, follow):
            return HttpResponse(response_pro.SerializeToString())
        else :
            initCommonErrorResponse(cmdId, 1, response_common)
            return HttpResponse(response_pro.SerializeToString())
    except Exception as error:
        log.error(str(error))
        initCommonErrorResponse(cmdId, 101, response_pro.common)
        return HttpResponse(response_pro.SerializeToString())

@csrf_exempt
def getOneTrend(request):
    cmdId = 10005
    request_pro = pilot_pb2.Request10005()
    response_pro = pilot_pb2.Response10005()
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

    userId = request_common.userid
    log.info("%d:%d,%s" % (cmdId,userId,str(request_params)))

    #构造返回
    try:
        response_common = response_pro.common
        response_data = response_pro.data
        initCommonResponse(0, 'success', cmdId, 0, response_common)
        if request_params.userId:
            if  userService.getOneTrend(request_params.pageIndex, request_params.userId, request_common.userid, response_data):
                return HttpResponse(response_pro.SerializeToString())
        elif userService.getOneTrend(request_params.pageIndex, request_common.userid, request_common.userid, response_data):
                return HttpResponse(response_pro.SerializeToString())
        else :
            initCommonErrorResponse(cmdId, 1, response_common)
            return HttpResponse(response_pro.SerializeToString())
    except Exception as error:
        log.error(str(error))
        initCommonErrorResponse(cmdId, 103, response_pro.common)
        return HttpResponse(response_pro.SerializeToString())

@csrf_exempt
def getMyCommentMessage(request):
    cmdId = 10006
    request_pro = pilot_pb2.Request10006()
    response_pro = pilot_pb2.Response10006()
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

    userId = request_common.userid
    log.info("%d:%d,%s" % (cmdId,userId,str(request_params)))
    #用户检验
    try:
        userService.userExist(request_common.userid,request_common.userkey)
    except:
        #未注册用户
        initCommonErrorResponse(cmdId, 101, response_pro.common)
        return HttpResponse(response_pro.SerializeToString())
    #构造返回
    try:
        response_common = response_pro.common
        response_data = response_pro.data
        initCommonResponse(0, 'success', cmdId, 0, response_common)
        if  userService.getMyCommentMessage(request_params.pageIndex,request_common.userid,response_data):
            return HttpResponse(response_pro.SerializeToString())
        else :
            initCommonErrorResponse(cmdId, 1, response_common)
            return HttpResponse(response_pro.SerializeToString())
    except Exception as error:
        log.error(str(error))
        initCommonErrorResponse(cmdId, 103, response_pro.common)
        return HttpResponse(response_pro.SerializeToString())

@csrf_exempt
def deleteCommentMassage(request):
    cmdId = 10007
    request_pro = pilot_pb2.Request10007()
    response_pro = pilot_pb2.Response10007()
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
    userId = request_common.userid
    log.info("%d:%d,%s" % (cmdId,userId,str(request_params)))
    #用户检验
    try:
        userService.userExist(request_common.userid,request_common.userkey)
    except:
        #未注册用户
        initCommonErrorResponse(cmdId, 101, response_pro.common)
        return HttpResponse(response_pro.SerializeToString())
    #构造返回
    try:
        response_common = response_pro.common
        response_data = response_pro.data
        initCommonResponse(0, 'success', cmdId, 0, response_common)

        if  userService.deleteCommentMassage(request_params.clearAll,request_params.messageIds,request_common.userid):
            return HttpResponse(response_pro.SerializeToString())
        else :
            initCommonErrorResponse(cmdId, 1, response_common)
            return HttpResponse(response_pro.SerializeToString())
    except Exception as error:
        log.error(str(error))
        initCommonErrorResponse(cmdId, 103, response_pro.common)
        return HttpResponse(response_pro.SerializeToString())

@csrf_exempt
def getMyXMoney(request):
    cmdId = 10008
    request_pro = pilot_pb2.Request10008()
    response_pro = pilot_pb2.Response10008()
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
    userId = request_common.userid
    log.info("%d:%d,%s" % (cmdId,userId,str(request_params)))
    #用户检验
    try:
        userService.userExist(request_common.userid,request_common.userkey)
    except:
        #未注册用户
        initCommonErrorResponse(cmdId, 101, response_pro.common)
        return HttpResponse(response_pro.SerializeToString())
    userId = request_common.userid
    log.info("%d:%d,%s" % (cmdId,userId,str(request_params)))
    #构造返回
    try:
        response_common = response_pro.common
        response_data = response_pro.data
        initCommonResponse(0, 'success', cmdId, 0, response_common)
        if  userService.getMyXMoney(request_common.userid,response_data):
            return HttpResponse(response_pro.SerializeToString())
        else :
            initCommonErrorResponse(cmdId, 1, response_common)
            return HttpResponse(response_pro.SerializeToString())
    except Exception as error:
        log.error(str(error))
        initCommonErrorResponse(cmdId, 103, response_pro.common)
        return HttpResponse(response_pro.SerializeToString())

#10009
@csrf_exempt
def getOnesUserFollow(request):
    cmdId = 10009
    request_pro = pilot_pb2.Request10009()
    response_pro = pilot_pb2.Response10009()
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
    userId = request_common.userid
    log.info("%d:%d,%s" % (cmdId,userId,str(request_params)))

    #构造返回

    try:
        response_common = response_pro.common
        response_data = response_pro.data
        initCommonResponse(0, 'success', cmdId, 0, response_common)
        if request_params.userId:
            if  userService.getOnesUserFollow(request_params.userId,  response_data):
                return HttpResponse(response_pro.SerializeToString())
        elif userService.getOnesUserFollow(request_common.userid, response_data):
                return HttpResponse(response_pro.SerializeToString())
        else :
            initCommonErrorResponse(cmdId, 1, response_common)
            return HttpResponse(response_pro.SerializeToString())
    except Exception as error:
        log.error(str(error))
        initCommonErrorResponse(cmdId, 103, response_pro.common)
        return HttpResponse(response_pro.SerializeToString())

#10010
@csrf_exempt
def getOnesUserFollowers(request):
    cmdId = 10010
    request_pro = pilot_pb2.Request10010()
    response_pro = pilot_pb2.Response10010()
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
    userId = request_common.userid
    log.info("%d:%d,%s" % (cmdId,userId,str(request_params)))
    #构造返回
    try:
        response_common = response_pro.common
        response_data = response_pro.data
        initCommonResponse(0, 'success', cmdId, 0, response_common)
        if request_params.userId:
            if  userService.getOnesUserFollowers( request_params.userId,  response_data):
                return HttpResponse(response_pro.SerializeToString())
        elif userService.getOnesUserFollowers(request_common.userid, response_data):
                return HttpResponse(response_pro.SerializeToString())
        else :
            initCommonErrorResponse(cmdId, 1, response_common)
            return HttpResponse(response_pro.SerializeToString())
    except Exception as error:
        log.error(str(error))
        initCommonErrorResponse(cmdId, 103, response_pro.common)
        return HttpResponse(response_pro.SerializeToString())

#10012
@csrf_exempt
def getUserDetail(request):
    cmdId = 10012
    request_pro = pilot_pb2.Request10012()
    response_pro = pilot_pb2.Response10012()
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

    #构造返回
    userId = request_common.userid
    log.info("%d:%d,%s" % (cmdId,userId,str(request_params)))

    try:
        response_common = response_pro.common
        response_data = response_pro.data
        initCommonResponse(0, 'success', cmdId, 0, response_common)
        if request_params.userId:
            if  userService.getUserDetail(request_params.userId, request_common.userid, response_data):
                log.info("%d %d %s" % (cmdId, request_params.userId, "成功"))
                return HttpResponse(response_pro.SerializeToString())
        elif userService.getUserDetail(request_common.userid,request_common.userid, response_data):
                return HttpResponse(response_pro.SerializeToString())
        else :
            initCommonErrorResponse(cmdId, 1, response_common)
            return HttpResponse(response_pro.SerializeToString())
    except Exception as error:
        log.error(str(error))
        initCommonErrorResponse(cmdId, 103, response_pro.common)
        return HttpResponse(response_pro.SerializeToString())

"""
搜索相关
"""

@csrf_exempt
def searchUser(request):
    cmdId = 10013
    request_pro = pilot_pb2.Request10013()
    response_pro = pilot_pb2.Response10013()
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
    userId = request_common.userid
    log.info("%d:%d,%s" % (cmdId,userId,str(request_params)))

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

#10014
@csrf_exempt
def searchGym(request):
    cmdId = 10014
    request_pro = pilot_pb2.Request10014()
    response_pro = pilot_pb2.Response10014()
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
    userId = request_common.userid
    log.info("%d:%d,%s" % (cmdId,userId,str(request_params)))

    #构造返回

    try:
        response_common = response_pro.common
        response_data = response_pro.data
        initCommonResponse(0, 'success', cmdId, 0, response_common)

        if  userService.searchGym(request_params.keyword, request_params.pageIndex, response_data):
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

#10015
@csrf_exempt
def getSearchKeys(request):
    cmdId = 10015
    request_pro = pilot_pb2.Request10015()
    response_pro = pilot_pb2.Response10015()
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

        if  userService.getSearchKeys(response_data):
            return HttpResponse(response_pro.SerializeToString())
        else :
            initCommonErrorResponse(cmdId, 1, response_common)
            return HttpResponse(response_pro.SerializeToString())
    except Exception as error:
        log.error(str(error))
        initCommonErrorResponse(cmdId, 103, response_pro.common)
        return HttpResponse(response_pro.SerializeToString())
    pass


@csrf_exempt
def getTrendBriefMessage(request):
    cmdId = 10017
    request_pro = pilot_pb2.Request10017()
    response_pro = pilot_pb2.Response10017()
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

    userId = request_common.userid
    log.info("%d:%d,%s" % (cmdId,userId,str(request_params)))
    #构造返回
    try:
        response_common = response_pro.common
        response_data = response_pro.data
        initCommonResponse(0, 'success', cmdId, 0, response_common)
        if  userService.getTrendBriefMessage(request_common.userid,response_data):
            return HttpResponse(response_pro.SerializeToString())
        else :
            initCommonErrorResponse(cmdId, 1, response_common)
            return HttpResponse(response_pro.SerializeToString())
    except Exception as error:
        log.error(str(error))
        initCommonErrorResponse(cmdId, 103, response_pro.common)
        return HttpResponse(response_pro.SerializeToString())


@csrf_exempt
def getBriefUser(request):
    cmdId = 10018
    request_pro = pilot_pb2.Request10018()
    response_pro = pilot_pb2.Response10018()
    try:
        protodata = request.read()
        log.info(protodata)
        request_pro.MergeFromString(protodata)
    except Exception as error:
        #如果读取异常直接返回一个error
        log.error('comunications failed')
        log.error(str(error))
        initCommonErrorResponse(cmdId, 0, response_pro.common)
        return HttpResponse(response_pro.SerializeToString())

    request_common = request_pro.common
    request_params = request_pro.params
    userId = request_common.userid
    log.info("%d:%d,%s" % (cmdId,userId,str(request_params)))
    #构造返回
    try:
        response_common = response_pro.common
        response_data = response_pro.data
        initCommonResponse(0, 'success', cmdId, 0, response_common)
        if request_params.userId:
            if  userService.getBriefUser(request_params.userId, request_common.userid, response_data):
                log.info("%d %d %s" % (cmdId, request_params.userId, "成功"))
                return HttpResponse(response_pro.SerializeToString())
        elif userService.getBriefUser(request_common.userid,request_common.userid, response_data):
                return HttpResponse(response_pro.SerializeToString())
        else :
            initCommonErrorResponse(cmdId, 1, response_common)
            return HttpResponse(response_pro.SerializeToString())
    except Exception as error:
        log.error(str(error))
        initCommonErrorResponse(cmdId, 103, response_pro.common)
        return HttpResponse(response_pro.SerializeToString())



@csrf_exempt
def getRecommendUser(request):
    cmdId = 10019
    request_pro = pilot_pb2.Request10019()
    response_pro = pilot_pb2.Response10019()
    try:
        protodata = request.read()
        log.info(protodata)
        request_pro.MergeFromString(protodata)
    except Exception as error:
        #如果读取异常直接返回一个error
        log.error('comunications failed')
        log.error(str(error))
        initCommonErrorResponse(cmdId, 0, response_pro.common)
        return HttpResponse(response_pro.SerializeToString())

    request_common = request_pro.common
    request_params = request_pro.params
    userId = request_common.userid
    log.info("%d:%d,%s" % (cmdId,userId,str(request_params)))
    longitude = request_params.longitude
    latitude = request_params.latitude
    #构造返回
    try:
        response_common = response_pro.common
        response_data = response_pro.data
        initCommonResponse(0, 'success', cmdId, 0, response_common)
        if  userService.getRecommendUser(userId, longitude , latitude , response_data):
            return HttpResponse(response_pro.SerializeToString())
        else :
            initCommonErrorResponse(cmdId, 1, response_common)
            return HttpResponse(response_pro.SerializeToString())
    except Exception as error:
        log.error(str(error))
        initCommonErrorResponse(cmdId, 103, response_pro.common)
        return HttpResponse(response_pro.SerializeToString())