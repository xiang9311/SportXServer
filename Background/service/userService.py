__author__ = '祥祥'
from Background.models import TblBriefUser, TblUserKey ,TblRongyunToken, TblTrendImage, TblTrend ,TblLikeTrend ,TblCommentMessage
from SportXServer import qiniuUtil, timeUtil, userKeyUtil ,rongcloud, log

def phoneExist(phone):
    users = TblBriefUser.objects.filter(userPhone=phone)
    if users:
        log.info('users is true')
        return True
    log.info('users is false')
    return False

def userExist(id,key):
    users = TblBriefUser.objects.filter(id = id)
    if users:
        log.info('users is true')
        return True
    log.info('users is false')
    return False

def register(phone, username, avatarKey, bucketName, password, sex, response_data):
    tblBriefUser = TblBriefUser()
    tblBriefUser.userName = username
    tblBriefUser.userAvatar = qiniuUtil.getBaseUrlByBucketName(bucketName) + avatarKey
    tblBriefUser.userPhone = phone
    tblBriefUser.userPW = password
    tblBriefUser.userSex = sex
    tblBriefUser.xMoney = 100
    tblBriefUser.signTime = timeUtil.getDatabaseTimeKeyOutOfDate()
    try :
        tblBriefUser.save()
    except Exception as e:
        log.error(str(e))
        print(e)
    # if not tblBriefUser.save():
    #     return False
    tblUserKey = TblUserKey()
    tblUserKey.user = tblBriefUser
    tblUserKey.userKey = userKeyUtil.getRandomUserKey()
    tblUserKey.outOfDateTime = timeUtil.getDatabaseTimeKeyOutOfDate()
    tblUserKey.save()

    #申请Rongtoken

    token = rongcloud.get_token(tblBriefUser.id,tblBriefUser.userName,tblBriefUser.userAvatar)
    #保存融云token
    Rong = TblRongyunToken()
    Rong.user = tblBriefUser
    Rong.token = token
    Rong.save()

    response_data.userId = tblBriefUser.id
    response_data.userKey = tblUserKey.userKey
    return True

#取得数据库的token
def getOldToken(userId):
    return TblRongyunToken.objects.get(user_id = userId).token

def getUserKey(userId):
    return TblUserKey.objects.get(user_id=userId).userKey

def getRongToken(userid):
    userinfo = TblBriefUser.objects.get(id = userid)
    token = rongcloud.get_token(userid, userinfo.userName, userinfo.userAvatar)
    #tokensave
    Rong = TblRongyunToken.objects.get(userid = userid)
    Rong.token = token
    Rong.save()
    return token

#登录
def login(phone ,password, response_data) :
    userinfo =  TblBriefUser.objects.get(userPhone = phone)
    #pw
    if userinfo.userPW == password:
        print(userinfo.userName)
        print(userinfo.id)
        response_briefuser = response_data.briefUser
        response_briefuser.userId = userinfo.id
        response_briefuser.userName = userinfo.userName
        response_briefuser.userAvatar = userinfo.userAvatar

        response_data.userKey = getUserKey(userinfo.id)
        response_data.rongyunToken = getOldToken(userinfo.id)
        response_data.sex = userinfo.userSex
        response_data.sign = userinfo.userSign
        response_data.phone = userinfo.userPhone

        return True
    return False

def searchUser(keyword, pageIndex, responseData):
    maxCountPerPage = 10
    searchedUsers = responseData.searchedUsers
    responseData.maxCountPerPage = maxCountPerPage
    tblBriefUsers = TblBriefUser.objects.filter(userName__contains=keyword)[pageIndex*10:(pageIndex+1)*10]
    for tblBriefUser in tblBriefUsers:
        searchedUser = searchedUsers.add()
        searchedUser.userId = tblBriefUser.id
        searchedUser.userName = tblBriefUser.userName
        searchedUser.userAvatar = tblBriefUser.userAvatar
        searchedUser.sign = tblBriefUser.userSign
        tblImages = TblTrendImage.objects.filter(createUser=tblBriefUser).order_by('-createTime', 'priority')[0:3]
        images = searchedUser.images
        for tblImage in tblImages:
            images.append(tblImage.url)
    return True

def updateUser(userId, userName, avatarKey, bucketName, sex, sign, phone, response_data):
    tblBriefUser = TblBriefUser.objects.get(id=userId)
    if userName:
        tblBriefUser.userName = userName
    if avatarKey:
        response_data.avatarUrl = qiniuUtil.getBaseUrlByBucketName(bucketName) + avatarKey
        tblBriefUser.userAvatar = qiniuUtil.getBaseUrlByBucketName(bucketName) + avatarKey
    if sex:
        tblBriefUser.userSex = sex
    if sign:
        tblBriefUser.userSign = sign
    if phone:
        tblBriefUser.userPhone = phone

    try:
        tblBriefUser.save()
    except Exception as error:
        log.info(str(error))
        return False

    return True

def guanzhuUser(fromUserId, toUserId, follow):
    if follow:
        tblBriefUser = TblBriefUser.objects.get(id=fromUserId)
        tblBriefUser.follow.add(TblBriefUser.objects.get(id=toUserId))
        try:
            tblBriefUser.save()
        except Exception as error:
            log.info(str(error))
            return False
    else:
        tblBriefUser = TblBriefUser.objects.get(id=fromUserId)
        tblBriefUser.follow.remove(TblBriefUser.objects.get(id=toUserId))
        try:
            tblBriefUser.save()
        except Exception as error:
            log.info(str(error))
            return False
    return True

def getOneTrend(pageIndex, userId, operationUser ,responseData):
    if getTrend(pageIndex, userId, operationUser ,responseData.trends,responseData.maxCountPerpage ):
        return True
    return False

def getTrend(pageIndex, userId, operationUser ,responseData_trends,responseData_maxCountPerPage ):
    maxCountPerPage = 10
    responseData_maxCountPerPage = maxCountPerPage
    response_trends = responseData_trends


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
def getUserDetail(userId, operateUser ,responseData):
    try :
        user = TblBriefUser.objects.get(id = userId)
    except Exception as e:
        log.error(str(e))
        return False

    response_user = responseData.detailUser
    response_user.userId = user.id
    response_user.userName = user.userName
    response_user.userAvatar = user.userAvatar
    response_user.sex = user.userSex
    try:
        response_user.sign = user.userSign
    except Exception as e:
        #
        pass
    response_user.trend = getTrend(1, userId, operateUser ,response_user.trends,response_user.trendMaxCountPerPage)#调用？
    response_user.trendMaxCountPerPage = 10  # 你之前那样调用不行呀
    if TblBriefUser.objects.get(id = operateUser).follow.get(id = userId):#这句话试试哈
        response_user.isFollowed = True
    else:
        response_user.isFollowed = False
    response_user.guanzhuCount = user.follow.count()
    response_user.fensiCount = user.tblbriefuser_set.count()
    response_user.trendCount = TblTrend.objects.filter(createUser_id= userId).count()

    return True
