from Background.models import TblBriefUser , TblTrend , TblBriefGym ,TblTrendImage ,TblLikeTrend ,TblTrendComment
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



def getTrendComment(trendId , pageIndex , responseData):
    #未处理maxCountPerPage!
    #没有return false
    maxCountPerPage = 10
    responseData.maxCountPerPage = maxCountPerPage
    response_comments = responseData.comments
    comments = TblTrendComment.objects.filter(trend_id = trendId)[pageIndex*10:(pageIndex+1)*10]
    for comment in comments:
        response_comment = response_comments.add()
        briefUser = response_comment.briefUser
        response_comment.commentId = comment.id
        response_comment.trendId = comment.trend.id
        response_comment.commentContent = comment.comment
        response_comment.toUserid = comment.toUserId
        response_comment.toUserName = TblBriefUser.objects.get(id = comment.toUserId).userName
        response_comment.createTime = comment.commentTime
        response_comment.gymName = comment.gym.gymName
        #createUser
        briefUser.userId = comment.createUser.id
        briefUser.userName = comment.createUser.userName
        briefUser.userAvatar = comment.createUser.userAvatar
    return True


def likeTrend(trendId, likeTrend):
    #TODO unfinish
    tblLikeTrend = TblLikeTrend()
    tblLikeTrend.createTime = timeUtil.getDatabaseTimeKeyOutOfDate()
    tblTrend = TblTrend.objects.get(id = trendId)
    tblLikeTrend.createUser = tblTrend.createUser#
    tblLikeTrend.trend = tblTrend
    tblLikeTrend.save()