from Background.models import TblBriefUser,TblTrend ,TblLikeTrend ,TblCommentMessage
from SportXServer import qiniuUtil, timeUtil ,log
#10005
def getOneTrend(pageIndex, userId, operationUser ,responseData):
    maxCountPerPage = 10
    responseData.maxCountPerPage = maxCountPerPage
    response_trends = responseData.trends


    try:
        followers = TblBriefUser.objects.get(id = userId).follow.all()
        #用in,shell中测试完成
        trends = TblTrend.objects.filter(createUser__in = followers).order_by('-createTime')[pageIndex*10:(pageIndex+1)*10]
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


#10006
def getMyCommentMessage(pageIndex , userId ,  responseData):

    maxCountPerPage = 10
    responseData.maxCountPerPage = maxCountPerPage
    response_comments = responseData.commentMessages
    try:
        Comments = TblCommentMessage.objects.filter(createUser_id = userId).order_by('-createTime')[pageIndex*10:(pageIndex+1)*10]
        for comment in Comments:
            response_comment = response_comments.add()
            response_comment.messageId = comment.id
            response_comment.messageContent = comment.content #消息的内容
            #这句话不懂啊
            if comment.createUser.userAvatar != "sportx": ## 消息所使用的头像 如果是"sportx"则是官方头像
                response_comment.avatar = comment.createUser.userAvatar
            else:
                response_comment.avatar = "sportx"
            response_comment.createTime = comment.createTime #创建时间 毫秒时间戳
            response_comment.trendId = comment.toTrend.id

    except Exception as e:
        log.error(str(e))
        return False
    return True

#10007
def deleteCommentMassage(cleanAll,messageIds, userId):
    try :
        if cleanAll:
            TblCommentMessage.objects.filter(toUser_id = userId).delete()
        else :
            TblCommentMessage.objects.filter(id__in = messageIds,toUserId=userId).delete()

    except Exception as e:
        log.error(str(e))
        return False
    return True

#10008
def getMyXMoney(userId , responseData):
    try :
        responseData.count = TblBriefUser.objects.get(id = userId).xMoney

    except Exception as e:
        log.error(str(e))
        return False
    return True


#1009
def getOnesUserFollow(userId, responseData):
    try :
        followers = TblBriefUser.objects.get(id = userId).follow.all()
    except Exception as e:
        log.error(str(e))
        return False

    response_users = responseData.briefUsers
    for follower in  followers:
        user = response_users.add()
        user.userId = follower.id
        user.userName = follower.userName
        user.userAvatar = follower.userAvatar

    return True


#10010
def getOnesUserFollowers(userId, responseData):
    #反查只有两个人，好难检测，但是方法是对的
    try :
        followers = TblBriefUser.objects.get(id = userId).tblbriefuser_set.all()
    except Exception as e:
        log.error(str(e))
        return False

    response_users = responseData.briefUsers
    for follower in  followers:
        user = response_users.add()
        user.userId = follower.id
        user.userName = follower.userName
        user.userAvatar = follower.userAvatar

    return True


#10012

def getUserDetail(userId, responseData):
    try :
        user = TblBriefUser.objects.get(id = userId)
    except Exception as e:
        log.error(str(e))
        return False

    response_user = responseData.detailUsers
    response_user.userId = user.id
    response_user.userName = user.userName
    response_user.userAvatar = user.userAvatar
    response_user.sex = user.userSex
    response_user.sign = user.userSign
    response_user.trend = #