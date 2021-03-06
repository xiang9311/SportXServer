from Background.models import TblBriefGym ,TblGyminfo ,TblGymEquipment ,TblCourse ,TblGymCard ,TblTrend ,TblTrendImage ,TblBriefUser, TblLikeTrend
from SportXServer import qiniuUtil, timeUtil, userKeyUtil ,rongcloud, log
from Background.dependency.geohash import encode, decode, neighbors

def getGymList(userId ,longitude , latitude ,pageIndex , responseData):
    maxCountPerPage = 10
    responseData.maxCountPerPage = maxCountPerPage
    response_gyms = responseData.briefGyms
    #todo:hashgeo
    sql = "SELECT * FROM Background_tblbriefgym " \
          "WHERE   ABS(latitude - "+str(latitude)+")<50/111 AND ABS(longitude - "+str(longitude)+")<50/111 " \
          "order by ACOS(SIN(('"+str(latitude)+"' * 3.1415) / 180 ) *SIN((latitude * 3.1415) / 180 ) " \
          "+COS(('"+str(latitude)+"' * 3.1415) / 180 ) * COS((latitude * 3.1415) / 180 ) *COS(('"+str(longitude)+"'* 3.1415) / 180 " \
          "- (longitude * 3.1415) / 180 ) ) * 6380 asc limit 10"
    try:
        if longitude and latitude:
            try:
                user = TblBriefUser.objects.get(id = userId)
                user.geohash = encode(latitude,longitude)
                user.save()
            except Exception as e:
                pass
        
        briefGyms = TblBriefGym.objects.raw(sql)[pageIndex*maxCountPerPage:(pageIndex+1)*maxCountPerPage]
        #todo:排序
        for briefGym in briefGyms:
            response_gym = response_gyms.add()
            response_gym.id = briefGym.id
            response_gym.gymName = briefGym.gymName
            response_gym.gymCover = TblGyminfo.objects.get(gym=briefGym,imageOrder__exact=1).image
            response_gym.place = briefGym.place
            response_gym.gymAvatar = briefGym.gymAvatar
            response_gym.latitude = briefGym.latitude
            response_gym.longitude = briefGym.longitude
            try:
                response_gym.eqm = briefGym.equipmentBrief
            except Exception as e:
                log.info('fixed exception %s' % str(e))
                response_gym.eqm = ''
    except Exception as e:
        log.info(str(e))
        return False

    return True


def getGymDetail(gymId,responseData):
    response_gym = responseData.detailGym.briefGym
    response_cover = responseData.detailGym.gymCovers
    response_users = responseData.briefUsers
    #gym
    briefGym = TblBriefGym.objects.get(id = gymId)
    response_gym.id = briefGym.id
    response_gym.gymName = briefGym.gymName
    response_gym.place = briefGym.place
    response_gym.gymAvatar = briefGym.gymAvatar
    response_gym.gymCover = TblGyminfo.objects.get(gym=briefGym,imageOrder__exact=1).image
    response_gym.latitude = briefGym.latitude
    response_gym.longitude = briefGym.longitude
    response_gym.eqm = briefGym.equipmentBrief
    responseData.detailGym.gymIntro = briefGym.gymIntro
    try:
        responseData.detailGym.courses = briefGym.courseBrief
    except:
        pass
    #todo 卡没存，先用美团价格，需要改协议
    responseData.detailGym.gymCards = "价格："+str(briefGym.price) +" ,某团价："+str(briefGym.meituan_price)
    #cover
    imgs = TblGyminfo.objects.filter(gym_id = briefGym.id)
    for img in imgs:
        response_cover.append(img.image)

    #briefUsers

    #使用位置查询usql =（用raw，自己写sql）
    try:
        users = TblBriefUser.objects.filter(lastShow_id = gymId)
        for user in users:
            response_user = response_users.add()
            response_user.userId = user.id
            response_user.userName = user.userName
            response_user.userAvatar = user.userAvatar
    except Exception as e:
        pass#没有user
    return True



def getRecommendGym(userId, gymId, longitude , latitude  , responseData):
    """
    没有合作标记位置，先用userId获取上次去过的体育馆
    :param longitude:
    :param latitude:
    :param responseData:
    :return:
    """
    try:

        if gymId:
            try:
                TblBriefUser.objects.get(id=userId).lastShow_id = gymId#还没加字段
            except Exception as e:
                pass
        else :
            if longitude and latitude:
                try:
                    user = TblBriefUser.objects.get(id = userId)
                    user.geohash = encode(latitude,longitude)
                    user.save()
                except Exception as e:
                    pass

            #todo:附近的体育馆id
            geoh = encode(latitude,longitude)
            i=8
            result = TblBriefGym.objects.filter(geohash__contains=geoh[0:i])
            while result == None:
                i=i-1
                result = TblBriefGym.objects.filter(geohash__contains=geoh[0:i])
            #result deal
            gymId = 4 #防止出错给了个4
            distance = 100000
            for gyms in result:
                if ((gyms.latitude-latitude)*(gyms.latitude-latitude)+(gyms.longitude - longitude)*(gyms.longitude - longitude) ) < distance:
                    distance = ((gyms.latitude-latitude)*(gyms.latitude-latitude)+(gyms.longitude - longitude)*(gyms.longitude - longitude) )
                    gymId = gyms.id


        briefGym = TblBriefGym.objects.get(id = gymId)
        response_gym = responseData.briefGym
        response_gym.id = briefGym.id
        response_gym.gymName = briefGym.gymName
        response_gym.place = briefGym.place
        response_gym.gymAvatar = briefGym.gymAvatar
        response_gym.gymCover = TblGyminfo.objects.get(gym_id=gymId,imageOrder__exact=1).image
        response_gym.latitude = briefGym.latitude
        response_gym.longitude = briefGym.longitude
        response_gym.eqm = briefGym.equipmentBrief

        try:
            users = TblBriefUser.objects.filter(lastShow_id = briefGym.id)
            responseData.userNum = users.count()
            responseData.trendNum = TblTrend.objects.filter(gym_id = briefGym.id).count()
            response_users = responseData.briefUsers
            for user in users:
                response_user = response_users.add()
                response_user.userId = user.id
                response_user.userName = user.userName
                response_user.userAvatar = user.userAvatar
        except Exception as e:
            log.info('users in recommend gym . info : %s' % str(e))
            pass

    except Exception as e:
        log.info('error : %s' % str(e))
        return False
    return True


def getGymTrend(userId, gymId, pageIndex , responseData):
    maxCountPerPage = 10
    responseData.maxCountPerPage = maxCountPerPage
    trends = responseData.trends
    try:
        tblTrends  = TblTrend.objects.filter(gym_id = gymId)
        for tblTrend in tblTrends:
            response_trend = trends.add()
            response_trend.id = tblTrend.id
            briefUser = response_trend.briefUser
            response_trend.createTime = timeUtil.dataBaseTime_toTimestemp(tblTrend.createTime)
            response_trend.gymId = gymId
            response_trend.gymName = tblTrend.gym.gymName
            response_trend.content = tblTrend.content
            response_trend.likeCount = tblTrend.likeCount
            response_trend.commentCount = tblTrend.commentCount
            images = response_trend.imgs
            tblImages = TblTrendImage.objects.filter(trend=tblTrend).order_by('priority')
            for tblImage in tblImages:
                images.append(tblImage.url)
            #createUser
            briefUser.userId = tblTrend.createUser.id
            briefUser.userName = tblTrend.createUser.userName
            briefUser.userAvatar = tblTrend.createUser.userAvatar

            try:
                if TblLikeTrend.objects.filter(trend=tblTrend, likeUser_id=userId):
                    response_trend.isLiked = True
                else:
                    response_trend.isLiked = False
            except Exception as e:
                response_trend.isLiked = False
                pass

    except Exception as e:
        return False
    return True

