from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .dependency import common_pb2,trend_pb2
from .service import  trendService
from .views import initCommonErrorResponse, initCommonResponse
from SportXServer import qiniuUtil, timeUtil ,log

"""
动态相关
"""

@csrf_exempt
def createTrend(request):
    """
    创建动态12001
    :param request:
    :return:
    """
    cmdId = 12001
    request_pro = trend_pb2.Request12001()
    response_pro = trend_pb2.Response12001()
    try:
        request_pro.MergeFromString(request.read())
    except:
        #如果读取异常直接返回一个error
        log.debug('comunications failed')
        initCommonErrorResponse(cmdId, 101, response_pro.common)
        return HttpResponse(response_pro.SerializeToString())

    request_common = request_pro.common
    request_params = request_pro.params

    try:
        response_common = response_pro.common
        response_data = response_pro.data
        initCommonResponse(0, 'success', cmdId, 0, response_common)

        if trendService.createTrend(request_params.content ,
                             request_common.userid ,
                             request_params.gymId,
                             request_params.bucketName ,
                             request_params.imageKeys):
            return HttpResponse(response_pro.SerializeToString())
        else:
            initCommonErrorResponse(cmdId, 1, response_common)
            return HttpResponse(response_pro.SerializeToString())

    except Exception as error:
        log.error(str(error))
        initCommonErrorResponse(cmdId, 101, response_pro.common)
        return HttpResponse(response_pro.SerializeToString())

@csrf_exempt
def getMyFollowTrends(request):
    """
    创建动态12002
    :param request:
    :return:
    """
    #TODO
    cmdId = 12002
    request_pro = trend_pb2.Request12002()
    response_pro = trend_pb2.Response12002()
    try:
        request_pro.MergeFromString(request.read())
    except:
        #如果读取异常直接返回一个error
        log.debug('comunications failed')
        initCommonErrorResponse(cmdId, 101, response_pro.common)
        return HttpResponse(response_pro.SerializeToString())


    request_common = request_pro.common
    request_params = request_pro.params


    try:
        response_common = response_pro.common
        response_data = response_pro.data
        initCommonResponse(0, 'success', cmdId, 0, response_common)

        if trendService.getMyFollowTrends(request_common.userid,request_params.pageIndex,response_data):
            return HttpResponse(response_pro.SerializeToString())
        else:
            initCommonErrorResponse(cmdId, 1, response_common)
            return HttpResponse(response_pro.SerializeToString())

    except Exception as error:
        log.error(str(error))
        initCommonErrorResponse(cmdId, 101, response_pro.common)
        return HttpResponse(response_pro.SerializeToString())

@csrf_exempt
def getTrendById(request):
    """
    创建动态12003
    message Response12003 {
	ResponseCommon common = 1;
	Data data = 2;
	message Data {
		Trend trends = 1;
	}
    }
    :param request:
    :return:
    """
    cmdId = 12003
    request_pro = trend_pb2.Request12003()
    response_pro = trend_pb2.Response12003()
    try:
        request_pro.MergeFromString(request.read())
    except:
        #如果读取异常直接返回一个error
        log.debug('comunications failed')
        initCommonErrorResponse(cmdId, 101, response_pro.common)
        return HttpResponse(response_pro.SerializeToString())


    request_common = request_pro.common
    request_params = request_pro.params


    try:
        response_common = response_pro.common
        response_data = response_pro.data
        initCommonResponse(0, 'success', cmdId, 0, response_common)

        if trendService.getTrend(request_params.trendId,response_data):
            return HttpResponse(response_pro.SerializeToString())
        else:
            initCommonErrorResponse(cmdId, 1, response_common)
            return HttpResponse(response_pro.SerializeToString())

    except Exception as error:
        log.error(str(error))
        initCommonErrorResponse(cmdId, 101, response_pro.common)
        return HttpResponse(response_pro.SerializeToString())

@csrf_exempt
def getTrendComment(request):
    """
    创建动态12004
    :param request:
    :return:
    """
    cmdId = 12004
    request_pro = trend_pb2.Request12004()
    response_pro = trend_pb2.Response12004()
    try:
        request_pro.MergeFromString(request.read())
    except:
        #如果读取异常直接返回一个error
        log.debug('comunications failed')
        initCommonErrorResponse(cmdId, 101, response_pro.common)
        return HttpResponse(response_pro.SerializeToString())
    request_common = request_pro.common
    request_params = request_pro.params
    try:
        response_common = response_pro.common
        response_data = response_pro.data
        initCommonResponse(0, 'success', cmdId, 0, response_common)

        if trendService.getTrendComment(request_params.trendId , request_params.pageIndex , response_data):
            return HttpResponse(response_pro.SerializeToString())
        else:
            initCommonErrorResponse(cmdId, 1, response_common)
            return HttpResponse(response_pro.SerializeToString())

    except Exception as error:
        log.error(str(error))
        initCommonErrorResponse(cmdId, 101, response_pro.common)
        return HttpResponse(response_pro.SerializeToString())

@csrf_exempt
def likeTrend(request):
    """
    创建动态12005
    :param request:
    :return:
    """
    cmdId = 12005
    request_pro = trend_pb2.Request12005()
    response_pro = trend_pb2.Response12005()
    try:
        request_pro.MergeFromString(request.read())
    except:
        #如果读取异常直接返回一个error
        log.debug('comunications failed')
        initCommonErrorResponse(cmdId, 101, response_pro.common)
        return HttpResponse(response_pro.SerializeToString())


    request_common = request_pro.common
    request_params = request_pro.params


    try:
        response_common = response_pro.common
        response_data = response_pro.data
        initCommonResponse(0, 'success', cmdId, 0, response_common)

        if trendService.likeTrend(request_params.trendId,
                             request_params.likeTrend):
            return HttpResponse(response_pro.SerializeToString())
        else:
            initCommonErrorResponse(cmdId, 1, response_common)
            return HttpResponse(response_pro.SerializeToString())

    except Exception as error:
        log.error(str(error))
        initCommonErrorResponse(cmdId, 101, response_pro.common)
        return HttpResponse(response_pro.SerializeToString())

@csrf_exempt
def commentTrend(request):
    """
    创建动态12006
    :param request:
    :return:
    """
    cmdId = 12006
    request_pro = trend_pb2.Request12006()
    response_pro = trend_pb2.Response12006()
    try:
        request_pro.MergeFromString(request.read())
    except:
        #如果读取异常直接返回一个error
        log.debug('comunications failed')
        initCommonErrorResponse(cmdId, 101, response_pro.common)
        return HttpResponse(response_pro.SerializeToString())


    request_common = request_pro.common
    request_params = request_pro.params


    try:
        response_common = response_pro.common
        response_data = response_pro.data
        initCommonResponse(0, 'success', cmdId, 0, response_common)

        if trendService.createComment(request_params.trendId,
                                      request_common.userid,
                                      request_params.toComment,
                                      request_params.toUser,
                                      request_params.content,
                                      request_params.gymId):
            return HttpResponse(response_pro.SerializeToString())
        else:
            initCommonErrorResponse(cmdId, 1, response_common)
            return HttpResponse(response_pro.SerializeToString())
    except Exception as error:
        log.error(str(error))
        initCommonErrorResponse(cmdId, 101, response_pro.common)
        return HttpResponse(response_pro.SerializeToString())

@csrf_exempt
def deleteComment(request):
    """
    创建动态12007
    :param request:
    :return:
    """
    cmdId = 12007
    request_pro = trend_pb2.Request12007()
    response_pro = trend_pb2.Response12007()
    try:
        request_pro.MergeFromString(request.read())
    except:
        #如果读取异常直接返回一个error
        log.debug('comunications failed')
        initCommonErrorResponse(cmdId, 101, response_pro.common)
        return HttpResponse(response_pro.SerializeToString())


    request_common = request_pro.common
    request_params = request_pro.params


    try:
        response_common = response_pro.common
        response_data = response_pro.data
        initCommonResponse(0, 'success', cmdId, 0, response_common)

        if trendService.deleteComment(request_params.trendId,request_params.commentId):
            return HttpResponse(response_pro.SerializeToString())
        else:
            initCommonErrorResponse(cmdId, 1, response_common)
            return HttpResponse(response_pro.SerializeToString())

    except Exception as error:
        log.error(str(error))
        initCommonErrorResponse(cmdId, 101, response_pro.common)
        return HttpResponse(response_pro.SerializeToString())

@csrf_exempt
def deleteTrend(request):
    """
    创建动态12008
    :param request:
    :return:
    """
    cmdId = 12008
    request_pro = trend_pb2.Request12008()
    response_pro = trend_pb2.Response12008()
    try:
        request_pro.MergeFromString(request.read())
    except:
        #如果读取异常直接返回一个error
        log.debug('comunications failed')
        initCommonErrorResponse(cmdId, 101, response_pro.common)
        return HttpResponse(response_pro.SerializeToString())


    request_common = request_pro.common
    request_params = request_pro.params


    try:
        response_common = response_pro.common
        response_data = response_pro.data
        initCommonResponse(0, 'success', cmdId, 0, response_common)

        if trendService.deleteTrend(request_params.trendId):
            return HttpResponse(response_pro.SerializeToString())
        else:
            initCommonErrorResponse(cmdId, 1, response_common)
            return HttpResponse(response_pro.SerializeToString())

    except Exception as error:
        log.error(str(error))
        initCommonErrorResponse(cmdId, 101, response_pro.common)
        return HttpResponse(response_pro.SerializeToString())