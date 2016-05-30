from Background.models import TblBriefGym ,TblGyminfo ,TblGymEquipment ,TblCourse ,TblGymCard
from SportXServer import qiniuUtil, timeUtil, userKeyUtil ,rongcloud, log


def getGymList(longitude , latitude ,pageIndex , responseData):
    response_gyms = responseData.briefGyms
    sql = "SELECT * FROM Background_tblbriefgym " \
          "WHERE ABS(latitude - "+str(latitude)+")<1/111 AND ABS(longitude - "+str(longitude)+")<1/111 " \
          "ORDER BY (-(latitude -"+str(latitude)+")^2 -(longitude - "+str(longitude)+")^2)"
    #todo test
    try:
        briefGyms = TblBriefGym.objects.raw(sql)#[pageIndex*maxCountPerPage:(pageIndex+1)*maxCountPerPage]
        for briefGym in briefGyms:
            response_gym = response_gyms.add()
            response_gym.id = briefGym.id
            response_gym.gymName = briefGym.gymName
            response_cover = response_gym.gymCover
            response_gym.place = briefGym.place
            response_gym.gymAvatar = briefGym.gymAvatar
            response_gym.latitude = briefGym.latitude
            response_gym.longitude = briefGym.longitude
            response_eqm = response_gym.equipments
            #cover
            imgs = TblGyminfo.objects.filter(gym_id = briefGym.id)
            for img in imgs:
                response_cover.append(img)
            #eqm
            eqms = TblGymEquipment.objects.filter(gym_id = briefGym.id)
            for eqm in eqms:
                if eqm:
                    response_eqm.name = eqm.name
                    response_eqm.count  = 1
    except Exception as e:
            return False

    return True


def getGym(gymId,responseData):
    response_gym = responseData.detailGym.briefGym
    response_courses = responseData.detailGym.courses
    response_gymCards = responseData.detailGym.gymCards
    #gym
    briefGym = TblBriefGym.objects.get(id = gymId)
    response_gym.id = briefGym.id
    response_gym.gymName = briefGym.gymName
    response_cover = response_gym.gymCover
    response_gym.place = briefGym.place
    response_gym.gymAvatar = briefGym.gymAvatar
    response_gym.latitude = briefGym.latitude
    response_gym.longitude = briefGym.longitude
    response_eqm = response_gym.equipments
    #cover
    imgs = TblGyminfo.objects.filter(gym_id = briefGym.id)
    for img in imgs:
        response_cover.append(img)
    #eqm
    eqms = TblGymEquipment.objects.filter(gym_id = briefGym.id)
    for eqm in eqms:
        if eqm:
            response_eqm.name = eqm.name
            response_eqm.count  = 1

    #course
    Courses = TblCourse.objects.filter(gym_id = briefGym.id)
    for Course in Courses:
        response_course = response_courses.add()
        response_course.name = Course.name
        response_course.week = Course.week
        response_course.courseTime.fromHour  = Course.fromHour
        response_course.courseTime.fromMinite = Course.fromMinite
        response_course.courseTime.toHour = Course.toHour
        response_course.courseTime.toMinite = Course.toMinite

    #card
    Cards = TblGymCard.objects.filter(gym_id = briefGym.id)
    for Card in Cards:
        response_gymCard = response_gymCards.add()
        response_gymCard.cardType = Card.cardType
        response_gymCard.price = Card.price

    #briefUsers
    """
    message BriefUser {
      int32 userId = 1;            // userid
      string userName = 2;          // 用户名
      string userAvatar = 3;       // 用户头像
    }
    """
    #todo 数据库结构
    response_user = responseData.briefUsers



