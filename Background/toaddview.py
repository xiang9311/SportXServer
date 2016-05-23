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


#TODO 10006 getMyCommentMessage
# message Request10006 {
# 	RequestCommon common = 1;
# 	Params params = 2;
# 	message Params {
# 		int32 pageIndex = 1;                         // 需要获取的页数，从0开始
# 	}
# }
#
# message Response10006 {
# 	ResponseCommon common = 1;
# 	Data data = 2;
# 	message Data {
# 		repeated CommentMessage commentMessages = 1;
# 		int32 maxCountPerPage = 2;                   // 每页的最大数量，如果messages小于该数量，则没有加载更多
# 	}
# }
#
# message CommentMessage {
# 	int32 messageId = 1;             // 消息的id
# 	string messageContent = 2;       // 消息的内容
# 	string avatar = 3;               // 消息所使用的头像 如果是"sportx"则是官方头像
# 	int64 createTime = 4;            // 创建时间 毫秒时间戳
# 	int32 trendId = 5;               // 消息对应的trendId
# }
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
        if request_params.userId:
            if  userService.getMyCommentMessage(request_params.pageIndex,response_data):
                log.info(cmdId+request_params.userId+"成功")
                return HttpResponse(response_pro.SerializeToString())
        else :
            initCommonErrorResponse(cmdId, 1, response_common)
            return HttpResponse(response_pro.SerializeToString())
    except Exception as error:
        log.error(str(error))
        initCommonErrorResponse(cmdId, 103, response_pro.common)
        return HttpResponse(response_pro.SerializeToString())
