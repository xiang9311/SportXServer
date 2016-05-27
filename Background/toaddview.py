from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .dependency import pilot_pb2
from .service import  toaddService as userService
from .views import initCommonErrorResponse, initCommonResponse
from SportXServer import qiniuUtil, timeUtil ,log

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

    log.info("搜索:数据解析成功" + str(request_params))

    #构造返回
    try:
        response_common = response_pro.common
        response_data = response_pro.data
        initCommonResponse(0, 'success', cmdId, 0, response_common)
        if  userService.searchGym(request_params.keyword, request_params.pageIndex, response_data):
            return HttpResponse(response_pro.SerializeToString())
        else :
            initCommonErrorResponse(cmdId, 1, response_common)
            return HttpResponse(response_pro.SerializeToString())
    except Exception as error:
        log.error(str(error))
        initCommonErrorResponse(cmdId, 103, response_pro.common)
        return HttpResponse(response_pro.SerializeToString())



#10018
# message Request10018 {
# 	RequestCommon common = 1;
# 	Params params = 2;
# 	message Params {
# 		int32 userId = 1;
# 	}
# }
#
# message Response10018 {
# 	ResponseCommon common = 1;
# 	Data data = 2;
# 	message Data {
# 		BriefUser briefUser = 1;
# 	}
# }
