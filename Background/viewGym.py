from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .dependency import common_pb2,trend_pb2,gym_pb2
from .service import  gymService , userService
from .views import initCommonErrorResponse, initCommonResponse
from SportXServer import qiniuUtil, timeUtil ,log

@csrf_exempt
def getGymList(request):
    """
    获取附近健身房列表
    :param request:
    :return:
    """
    cmdId = 13001
    request_pro = gym_pb2.Request13001()
    response_pro = gym_pb2.Response13001()
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
        longitude = request_params.longitude
        latitude = request_params.latitude
        if gymService.getGymList(longitude , latitude , request_params.pageIndex , response_data):
            return HttpResponse(response_pro.SerializeToString())
        else:
            initCommonErrorResponse(cmdId, 1, response_common)
            return HttpResponse(response_pro.SerializeToString())

    except Exception as error:
        log.error(str(error))
        initCommonErrorResponse(cmdId, 101, response_pro.common)
        return HttpResponse(response_pro.SerializeToString())


@csrf_exempt
def getGymList(request):
    """
    获取附近健身房列表
    :param request:
    :return:
    """
    cmdId = 13002
    request_pro = gym_pb2.Request13002()
    response_pro = gym_pb2.Response13002()
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
        longitude = request_params.longitude
        latitude = request_params.latitude
        if gymService.getGym(request_params.gymId, response_data):
            return HttpResponse(response_pro.SerializeToString())
        else:
            initCommonErrorResponse(cmdId, 1, response_common)
            return HttpResponse(response_pro.SerializeToString())

    except Exception as error:
        log.error(str(error))
        initCommonErrorResponse(cmdId, 101, response_pro.common)
        return HttpResponse(response_pro.SerializeToString())