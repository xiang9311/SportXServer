from Background.models import TblBriefUser,TblTrend ,TblLikeTrend
from SportXServer import qiniuUtil, timeUtil ,log

def getOneTrend(pageIndex, userId, operationUser ,responseData):
    trend = TblTrend.objects.get(createUser__id = userId)
    maxCountPerPage = 10
    responseData.maxCountPerPage = maxCountPerPage
    response_trends = responseData.trends

    followers = TblBriefUser.objects.get(id = userId).follow.all()
    #用in,shell中测试完成
    trends = TblTrend.objects.filter(createUser__in = followers)[pageIndex*10:(pageIndex+1)*10]
    try:
        for trend in trends:
            response_trend = response_trends.add()
            briefUser = response_trends.briefUser
            response_trend.createTime = trend.createTime
            response_trend.gymId = trend.gym.id
            response_trend.gymName = trend.gym.gymName
            response_trend.content = trend.content
            response_trend.likeCount = trend.likeCount
            response_trend.commentCount = trend.commentCount
            #createUser
            briefUser.userId = trend.createUser.id
            briefUser.userName = trend.createUser.userName
            briefUser.userAvatar = trend.createUser.userAvatar
            if TblLikeTrend.objects.get(trend_id= trend.id ,likeUser_id = operationUser):
                response_trend.isLiked = True
            else:
                response_trend.isLiked = False


    except Exception as e:
        log.error(str(e))
        return False
    return True
