from django.db import models
from enum import Enum
# Create your models here.
#BrirfUser
# TODO:
# 关于Float设置：  
# max_digits
# 必填，数字长度
# decimal_places
# 必填，即有效位数

"""
用户相关表
"""

"""
用户表
"""
class TblBriefUser(models.Model):
    userName = models.CharField(max_length = 30)
    userPhone = models.CharField(max_length = 13)
    userPW = models.CharField(max_length = 36)
    userCover = models.URLField()
    userSex = models.BooleanField()
    userSign = models.CharField(max_length = 30)
    xMoney = models.IntegerField()
    follow = models.ManyToManyField("self", symmetrical=False)        # 这里存的是我关注的人
    signTime = models.DateTimeField()

class TblUserKey(models.Model):
    user = models.ForeignKey(TblBriefUser)
    userKey = models.CharField(max_length = 36)
    outOfDateTime = models.DateTimeField()

class TblRongyunToken(models.Model):
    user = models.ForeignKey(TblBriefUser)
    token = models.CharField(max_length = 100)

"""
场馆表
"""
class TblBriefGym(models.Model):
    gymName = models.CharField(max_length = 30)
    gymAvatar = models.URLField()#image
    place = models.CharField(max_length = 100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    gymIntro = models.CharField(max_length = 500)
    createTime = models.DateTimeField()

"""
平台定义的所有设置
"""
class TblAllEquipment(models.Model):
    name = models.CharField(max_length = 30)
    equipmentType = models.IntegerField()
    createTime = models.DateTimeField()

"""
用户动态表
"""
class TblTrend(models.Model):
    content  =  models.CharField(max_length = 30)
    createUser = models.ForeignKey(TblBriefUser)
    gym = models.ForeignKey(TblBriefGym)
    likeCount = models.IntegerField()
    commentCount = models.IntegerField()
    createTime = models.DateTimeField()

"""
动态的评论表
"""
class TblTrendComment(models.Model):
    trend = models.ForeignKey(TblTrend)
    comment = models.CharField(max_length = 300)
    createUser = models.ForeignKey(TblBriefUser)
    toUserId = models.IntegerField()
    gym = models.ForeignKey(TblBriefGym)
    commentTime = models.DateTimeField()

"""
动态的图片表
"""
class TblTrendImage(models.Model):
    trend = models.ForeignKey(TblTrend)
    url = models.URLField()
    createUser = models.ForeignKey(TblBriefUser)
    priority = models.IntegerField()
    createTime = models.DateTimeField()

"""
X币数量变化相关表
"""
class TblXMoneyLog(models.Model):
    createUser = models.ForeignKey(TblBriefUser)
    xMoneyChanged = models.IntegerField()
    reason = models.CharField(max_length = 30)
    createTime = models.DateTimeField()

"""
点赞表
"""
class TblLikeTrend(models.Model):
    trend = models.ForeignKey(TblTrend)
    createUser = models.ForeignKey(TblBriefUser)
    createTime = models.DateTimeField()

"""
曾经关注表
"""
class TblEverFollow(models.Model):
    followedUserId = models.IntegerField()         # 被关注者
    createUserId = models.IntegerField()             # 关注者
    followTime = models.DateTimeField()

"""
评论消息表
"""
class TblCommentMessage(models.Model):
    content = models.CharField(max_length=200)
    toTrend = models.ForeignKey(TblTrend)
    toUserId = models.IntegerField()
    createUser = models.ForeignKey(TblBriefUser)
    createTime = models.DateTimeField()

"""
场馆相关
"""

"""
场馆设施表
"""
class TblGymEquipment(models.Model):
    equipment = models.ForeignKey(TblAllEquipment)
    name = models.CharField(max_length = 30)
    equipmentType = models.IntegerField()
    eIntro = models.CharField(max_length = 100)
    gym = models.ForeignKey(TblBriefGym)
    createTime = models.DateTimeField()

"""
课程
"""
class TblCourse(models.Model):
    name =models.CharField(max_length = 30)
    week = models.IntegerField()
    fromHour = models.IntegerField()
    fromMinite = models.IntegerField()
    toHour = models.IntegerField()
    toMinite = models.IntegerField()
    gym = models.ForeignKey(TblBriefGym)
    createTime = models.DateTimeField()

"""
场馆卡
"""
class TblGymCard(models.Model):
    cardType = models.IntegerField()
    price = models.FloatField()
    gym = models.ForeignKey(TblBriefGym)
    createTime = models.DateTimeField()

"""
场馆介绍图片
"""
class TblGyminfo(models.Model):
    image = models.URLField()
    gym = models.ForeignKey(TblGymCard)
    imageOrder = models.IntegerField()
    createTime = models.DateTimeField()


"""
搜索相关
"""

class TblSearchKeywords(models.Model):
    keyword = models.CharField(max_length = 100)
    usedTimes = models.IntegerField()

# class  CardType(Enum):
#    Once = 0;  # 一次 体验卡
#    Month = 1;    # 月卡
#    Quarter = 2;  # 季度卡

# enum EquipmentType {
#   PAO_BU_JI = 0;  # 跑步机
#   LIN_YU_FANG = 1;      # 淋浴房
# }

# enum Sex{
#   MALE = 0;    # 男性
#   FEMALE = 1;    # 女性
# }
# class Banner(models.Model):
#     #??type 
#     # URL = 0;     # 跳转url
#     #TREND = 1;  # 跳转动态
#     #USER = 2;    # 用户
#     banid = models.IntegerField(primary_key=True)
#     coverUrl = models.CharField(max_length = 30)
#     bantype = models.IntegerField()
#     webUrl = models.CharField(max_length = 30)
#     trendId = models.IntegerField()
#     userid = models.IntegerField()

#关于枚举http:#codego.net/1168/ 的方法