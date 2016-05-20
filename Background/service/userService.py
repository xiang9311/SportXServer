__author__ = '祥祥'
from Background.models import TblBriefUser, TblUserKey ,TblRongyunToken, TblTrendImage
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

def isRegister(id,key):
    return True

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
        tblImages = TblTrendImage.objects.filter(createUser=tblBriefUser).order_by('createTime')[0:3]
        images = searchedUser.images
        for tblImage in tblImages:
            image = images.add()
            image = tblImage.url
    return True

def updateUser(userId, userName, avatarKey, bucketName, sex, sign, phone, response_data):
    tblBriefUser = TblBriefUser.object.get(id = userId)
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