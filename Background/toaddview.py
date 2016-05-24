from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .dependency import pilot_pb2
from .service import  toaddService as userService
from .views import initCommonErrorResponse, initCommonResponse
from SportXServer import qiniuUtil, timeUtil ,log


def getOneTrend(request):
    # message Response10005 {
    # 	ResponseCommon common = 1;
    # 	Data data = 2;
    # 	message Data {
    # 		repeated Trend trends = 1;
    # 		int32 maxCountPerPage = 2;                   // 每页的最大数量，如果trends小于该数量，则没有加载更多
    # 	}
    # }
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

    log.info("搜索:数据解析成功" + str(request_params))

    #构造返回

    try:
        response_common = response_pro.common
        response_data = response_pro.data
        initCommonResponse(0, 'success', cmdId, 0, response_common)
        if request_params.userId:
            if  userService.getOneTrend(request_params.pageIndex, request_params.userId, request_common.userid, response_data):
                log.info(cmdId+request_params.userId+"成功")
                return HttpResponse(response_pro.SerializeToString())
        elif userService.getOneTrend(request_params.pageIndex, request_common.userid, request_common.userid, response_data):
                log.info(cmdId+"成功")
                return HttpResponse(response_pro.SerializeToString())
        else :
            initCommonErrorResponse(cmdId, 1, response_common)
            return HttpResponse(response_pro.SerializeToString())
    except Exception as error:
        log.error(str(error))
        initCommonErrorResponse(cmdId, 103, response_pro.common)
        return HttpResponse(response_pro.SerializeToString())



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

    log.info("搜索:数据解析成功" + str(request_params))

    #构造返回

    try:
        response_common = response_pro.common
        response_data = response_pro.data
        initCommonResponse(0, 'success', cmdId, 0, response_common)
        if  userService.getMyCommentMessage(request_params.pageIndex,request_common.userid,response_data):
            log.info(cmdId+request_params.userId+"成功")
            return HttpResponse(response_pro.SerializeToString())
        else :
            initCommonErrorResponse(cmdId, 1, response_common)
            return HttpResponse(response_pro.SerializeToString())
    except Exception as error:
        log.error(str(error))
        initCommonErrorResponse(cmdId, 103, response_pro.common)
        return HttpResponse(response_pro.SerializeToString())


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

    log.info("搜索:数据解析成功" + str(request_params))

    #构造返回

    try:
        response_common = response_pro.common
        response_data = response_pro.data
        initCommonResponse(0, 'success', cmdId, 0, response_common)
        if  userService.deleteCommentMassage(request_params.cleanAll,request_params.messageids,request_common.userid):
            log.info(cmdId+request_params.userId+"成功")
            return HttpResponse(response_pro.SerializeToString())
        else :
            initCommonErrorResponse(cmdId, 1, response_common)
            return HttpResponse(response_pro.SerializeToString())
    except Exception as error:
        log.error(str(error))
        initCommonErrorResponse(cmdId, 103, response_pro.common)
        return HttpResponse(response_pro.SerializeToString())


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

    log.info("搜索:数据解析成功" + str(request_params))

    #构造返回

    try:
        response_common = response_pro.common
        response_data = response_pro.data
        initCommonResponse(0, 'success', cmdId, 0, response_common)
        if  userService.getMyXMoney(request_common.userid,response_data):
            log.info(cmdId+request_params.userId+"成功")
            return HttpResponse(response_pro.SerializeToString())
        else :
            initCommonErrorResponse(cmdId, 1, response_common)
            return HttpResponse(response_pro.SerializeToString())
    except Exception as error:
        log.error(str(error))
        initCommonErrorResponse(cmdId, 103, response_pro.common)
        return HttpResponse(response_pro.SerializeToString())

#10009
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

    log.info("搜索:数据解析成功" + str(request_params))

    #构造返回

    try:
        response_common = response_pro.common
        response_data = response_pro.data
        initCommonResponse(0, 'success', cmdId, 0, response_common)
        if request_params.userId:
            if  userService.getOnesUserFollow(request_params.userId,  response_data):
                log.info(cmdId+request_params.userId+"成功")
                return HttpResponse(response_pro.SerializeToString())
        elif userService.getOnesUserFollow(request_common.userid, response_data):
                log.info(cmdId+"成功")
                return HttpResponse(response_pro.SerializeToString())
        else :
            initCommonErrorResponse(cmdId, 1, response_common)
            return HttpResponse(response_pro.SerializeToString())
    except Exception as error:
        log.error(str(error))
        initCommonErrorResponse(cmdId, 103, response_pro.common)
        return HttpResponse(response_pro.SerializeToString())


#10010
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

    log.info("搜索:数据解析成功" + str(request_params))

    #构造返回

    try:
        response_common = response_pro.common
        response_data = response_pro.data
        initCommonResponse(0, 'success', cmdId, 0, response_common)
        if request_params.userId:
            if  userService.getOnesUserFollowers( request_params.userId,  response_data):
                log.info(cmdId+request_params.userId+"成功")
                return HttpResponse(response_pro.SerializeToString())
        elif userService.getOnesUserFollowers(request_common.userid, response_data):
                log.info(cmdId+"成功")
                return HttpResponse(response_pro.SerializeToString())
        else :
            initCommonErrorResponse(cmdId, 1, response_common)
            return HttpResponse(response_pro.SerializeToString())
    except Exception as error:
        log.error(str(error))
        initCommonErrorResponse(cmdId, 103, response_pro.common)
        return HttpResponse(response_pro.SerializeToString())


#10012
def getUserDetail(request):
    cmdId = 10012
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

    log.info("搜索:数据解析成功" + str(request_params))

    #构造返回

    try:
        response_common = response_pro.common
        response_data = response_pro.data
        initCommonResponse(0, 'success', cmdId, 0, response_common)
        if request_params.userId:
            if  userService.getUserDetail(request_params.userId,  response_data):
                log.info(cmdId+request_params.userId+"成功")
                return HttpResponse(response_pro.SerializeToString())
        elif userService.getUserDetail(request_common.userid, response_data):
                log.info(cmdId+"成功")
                return HttpResponse(response_pro.SerializeToString())
        else :
            initCommonErrorResponse(cmdId, 1, response_common)
            return HttpResponse(response_pro.SerializeToString())
    except Exception as error:
        log.error(str(error))
        initCommonErrorResponse(cmdId, 103, response_pro.common)
        return HttpResponse(response_pro.SerializeToString())