from Background.models import TblBriefUser,TblTrend ,TblLikeTrend ,TblCommentMessage,TblBriefGym
from SportXServer import qiniuUtil, timeUtil ,log


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




