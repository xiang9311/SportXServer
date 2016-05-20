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
    response_pro = trend_pb2.Request12001()
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


def getMyFollowTrends(request):
    """
    创建动态12002
    :param request:
    :return:
    """
    #TODO


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
    response_pro = trend_pb2.Request12003()
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