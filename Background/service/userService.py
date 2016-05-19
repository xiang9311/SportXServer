__author__ = '祥祥'
from Background.models import TblBriefUser, TblUserKey ,TblRongyunToken
from SportXServer import qiniuUtil, timeUtil, userKeyUtil ,rongcloud

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
def getOldToken(userid):
    return TblRongyunToken.objects.get(user = userid).token

def getRongToken(userid):
    userinfo = TblBriefUser.objects.get(id = userid)
    token = rongcloud.get_token(userid,userinfo.userName,userinfo.userAvatar)
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
        userKey = response_data.userKey
        rongyunToken = response_data.rongyunToken
        #DATA_BRIEFUSER
        response_briefuser.userId = userinfo.id
        response_briefuser.userName = userinfo.userName
        response_briefuser.userAvatar = userinfo.userAvatar
        rongyunToken = getOldToken(userinfo.id)#获取已有Token
        return True
    return False 
def isRegister(id,key):
    return True




