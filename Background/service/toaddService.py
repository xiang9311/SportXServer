from Background.models import TblBriefUser,TblTrend ,TblLikeTrend ,TblCommentMessage
from SportXServer import qiniuUtil, timeUtil ,log
#10017
def getTrendBriefMessage(userId ,  responseData):
    try:
        hadRead = TblBriefUser.objects.get(id = userId).hadReadMessage
        comments = TblCommentMessage.objects.filter(toUserId=userId , id__gt=hadRead).order_by('-id')
    except Exception as e:
        log.error(str(e))
        return False
    briefMessage = responseData.trendBriefMessage
    briefMessage.lastAvatar = TblBriefUser.objects.get(id = comments[0].createUser.id).userAvatar
    briefMessage.count = comments.count()
    return True


#10014
#todo img eqm isCoop
def searchGym(keyword,pageIndex,responseData):
    maxCountPerPage = 10
    response_gyms = responseData.briefGyms
    responseData.maxCountPerPage = maxCountPerPage
    tblBriefGyms = TblBriefGym.objects.filter(gymName__contains = keyword)[pageIndex*10:(pageIndex+1)*10]
    for tblBriefGym in tblBriefGyms:
        response_gym = response_gyms.add()
        response_gym.id = tblBriefGym.id
        response_gym.gymName = tblBriefGym.gymName
        img = response_gym.gymCover#没有这个字段
        response_gym.place = tblBriefGym.place
        response_gym.gymAvatar = tblBriefGym.gymAvatar
        response_gym.latitude = tblBriefGym.latitude
        response_gym.longitude = tblBriefGym.longitude
        response_gym.isCoop = False#没有这个字段
        eqm = response_gym.equipments
        # for tblImage in tblImages:
        #     images.append(tblImage.url)