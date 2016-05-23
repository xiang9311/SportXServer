from Background.models import TblBriefUser , TblTrend , TblBriefGym ,TblTrendImage ,TblLikeTrend ,TblTrendComment,TblCommentMessage
from SportXServer import qiniuUtil, timeUtil ,log


def createTrend(content , userId ,gymId, bucketName , imageKeys):
    tblTrend = TblTrend()
    tblTrend.content = content
    tblTrend.createUser = TblBriefUser.objects.get(id = userId)
    tblTrend.likeCount = 0
    tblTrend.commentCount = 0
    if gymId:
        tblTrend.gym = TblBriefGym.objects.get(id = gymId)
    tblTrend.createTime = timeUtil.getDatabaseTimeNow()
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
        tblTrendImage.createUser = tblTrend.createUser
        tblTrendImage.priority = i# 次序
        tblTrendImage.createTime = tblTrend.createTime
        try:
            tblTrendImage.save()
        except Exception as e:
            log.error(str(e))
            return False
    return True


def getMyFollowTrends(userId,pageIndex,responseData):
    #未处理maxCountPerPage!
    #过程有问题
    maxCountPerPage = 10
    responseData.maxCountPerPage = maxCountPerPage
    response_trends = responseData.trends

    user = TblBriefUser.objects.get(id = userId)

    followers = user.follow.all().values("id")
    qList = list(followers)
    sList = set([s['id'] for s in qList])
    sList.add(userId)
    trends = TblTrend.objects.filter(createUser_id__in = sList).order_by('-createTime')[pageIndex*maxCountPerPage:(pageIndex+1)*maxCountPerPage]

    try:
        for trend in trends:
            response_trend = response_trends.add()
            response_trend.id = trend.id
            trend_user = response_trend.briefUser
            response_trend.createTime = int(timeUtil.dataBaseTime_toTimestemp(trend.createTime) * 1000)
            #gym名字需要查询
            try:
                # 有可能没有加gym
                response_trend.gymId = trend.gym.id
                response_trend.gymName = trend.gym.gymName
            except Exception as e:
                pass
            response_trend.content = trend.content
            response_trend.likeCount = trend.likeCount
            response_trend.commentCount = trend.commentCount
            #createuser
            trend_user.userId = trend.createUser.id
            trend_user.userName = trend.createUser.userName
            trend_user.userAvatar = trend.createUser.userAvatar

            #images
            images = response_trend.imgs
            tblImages = TblTrendImage.objects.filter(trend=trend).order_by('priority')
            for tblImage in tblImages:
                images.append(tblImage.url)
            try:
                # 查询不到会报异常
                if  TblLikeTrend.objects.get(trend=trend, likeUser=user):
                    response_trend.isLiked = True
                else :
                    response_trend.isLiked = False
            except Exception as e:
                response_trend.isLiked = False
    except Exception as e:
        log.error(str(e))
        return False
    return True


def getTrend(trendId ,responseDate, userId):
    trend = TblTrend.objects.get(id = trendId)
    response_trend = responseDate.trends
    response_trend.id = trendId
    trend_user = response_trend.briefUser
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
    if TblLikeTrend.objects.get(trend=trend, likeUser_id=userId):
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
    try:
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
    except Exception as e:
        log.error(str(e))
        return False
    return True


def likeTrend(trendId, likeTrend, userId):
    tblLikeTrend = TblLikeTrend()
    tblLikeTrend.createTime = timeUtil.getDatabaseTimeKeyOutOfDate()
    tblTrend = TblTrend.objects.get(id = trendId)
    tblUser = TblBriefUser.objects.get(id = userId)
    tblLikeTrend.createUser = tblUser#
    tblLikeTrend.trend = tblTrend
    try:
        tblLikeTrend.save()
    except Exception as e:
        log.error(str(e))
        return False
    return True


def createComment(trendId,createUser,toComment,toUser,content,gymId):
    #评论表
    tblTrendComment = TblTrendComment()
    tblTrendComment.trend = TblTrend.objects.get(id = trendId)
    tblTrendComment.comment = content
    tblTrendComment.createUser = TblBriefUser.objects.get(id =createUser)
    tblTrendComment.toUserId = toUser
    tblTrendComment.toCommentId = toComment
    tblTrendComment.gym = TblBriefGym.objects.get(id = gymId)
    tblTrendComment.commentTime = timeUtil.getDatabaseTimeKeyOutOfDate()
    #消息表
    tblTrendCommentMassage = TblCommentMessage()
    tblTrendCommentMassage.content = content
    tblTrendCommentMassage.toTrend = TblTrend.objects.get(id = trendId)
    tblTrendCommentMassage.toUserId = toUser
    tblTrendCommentMassage.createUser = TblBriefUser.objects.get(id =createUser)
    tblTrendCommentMassage.createTime = timeUtil.getDatabaseTimeKeyOutOfDate()
    try:
        tblTrendComment.save()
        tblTrendCommentMassage.save()
    except Exception as e:
        log.error(str(e))
        return False
    return True


def deleteComment(trendId,commentId):
    try:
        TblTrendComment.objects.filter(trend_id = trendId,id = commentId).delete()
        TblCommentMessage.objects.filter(toTrend_id = trendId , id = commentId).delete()
    except Exception as e:
        log.error(str(e))
        return False
    return True


def deleteTrend(trendId):
    try:
        TblTrend.objects.get(id = trendId).delete()
        TblTrendComment.objects.filter(trend_id = trendId).delete()
        TblLikeTrend.objects.filter(trend_id = trendId ).delete()
        TblCommentMessage.objects.filter(toTrend_id = trendId).delete()
    except Exception as e:
        log.error(str(e))
        return False
    return True



