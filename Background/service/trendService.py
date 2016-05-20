from Background.models import TblBriefUser , TblTrend , TblBriefGym ,TblTrendImage ,TblLikeTrend
from SportXServer import qiniuUtil, timeUtil ,log

def createTrend(content , userid ,gymid, bucketName , imageKeys):
    tblTrend = TblTrend()
    tblTrend.content = content
    tblTrend.createUser = TblBriefUser.objects.get(id = userid)
    tblTrend.likeCount = 0
    tblTrend.commentCount = 0
    if gymid != None:
        tblTrend.gym = TblBriefGym.objects.get(id = gymid)
    tblTrend.createTime = timeUtil.getDatabaseTimeKeyOutOfDate()
    try:
        tblTrend.save()
    except Exception as e:
        log.error(str(e))
        return False
    #image
    for i in range(0 , len(imageKeys)):
        tblTrendImage = TblTrendImage()
        tblTrendImage.trend = tblTrend
        tblTrendImage.url = qiniuUtil.getBaseUrlByBucketName(bucketName) + imageKeys[i] #qiniukey?
        tblTrendImage.createUser = tblTrend.createUser()
        tblTrendImage.priority = i# 次序
        tblTrendImage.createTime = tblTrend.createTime
        try:
            tblTrendImage.save()
        except Exception as e:
            log.error(str(e))
            return False
    return True


def getTrend(trendId ,responseDate):
    trend = TblTrend.objects.get(id = trendId)
    response_trend = responseDate.trends
    response_trend.id = trendId
    trend_user = response_trend.briedUser
    response_trend.createTime = trend.createTime
    #gym名字需要查询
    response_trend.gymId = trend.gym.id
    response_trend.gymName = trend.gym.gymName
    response_trend.content = trend.content
    response_trend.likeCount = trend.likeCount
    response_trend.commentCount = trend.commentCount
    #createuser
    trend_user.userId = trend.createUser.id
    trend_user.userName = trend.createUser.userName
    trend_user.userAvatar = trend.createUser.userAvatar
    if TblLikeTrend.objects.get(trend_id= trendId):
        response_trend.isLiked = True
    else:
        response_trend.isLiked = False
