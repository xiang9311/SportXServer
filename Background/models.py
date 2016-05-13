from django.db import models
from enum import Enum
# Create your models here.
#request
class RequestCommon(models.Model):
    userid = models.IntegerField
    userkey = models.CharField(max_length = 30)
    cmdid = models.IntegerField
    timestamp = models.DateField
    version =  models.CharField(max_length = 30)
    platform = models.IntegerField

  #response
class ResponseCommon(models.Model):
    code = models.IntegerField
    message = models.CharField(max_length = 30)
    cmdid = models.IntegerField
    timestamp = models.DateTimeField
    userid = models.IntegerField
#BrirfUser
class BriefUser(models.Model):
    userid = models.IntegerField
    userName = models.CharField(max_length = 30)
    userAvatar = models.CharField(max_length = 30)

#Trend
class Trend(models.Model):
    id = models.IntegerField
    briefUser = models.ManyToManyField(BriefUser)
    createTime = models.DateTimeField()
    gymid = models.IntegerField
    gymName =  models.CharField(max_length = 30)
    content  =  models.CharField(max_length = 30)
    imgs =  models.ImageField
    likeCount = models.IntegerField
    commentCount = models.IntegerField
    isLiked = models.BooleanField

class Banner(models.Model):
    #??type 
    # URL = 0;     # 跳转url
    #TREND = 1;  # 跳转动态
    #USER = 2;    # 用户
    id = models.IntegerField
    coverUrl = models.CharField(max_length = 30)
    type = models.IntegerField
    webUrl = models.CharField(max_length = 30)
    trendId = models.IntegerField
    userid = models.IntegerField



class BriefGym(models.Model):
    id = models.IntegerField
    gymName = models.CharField(max_length = 30)
    gymCover = models.ImageField
    place = models.CharField
    gymAvatar = models.CharField(max_length = 30)
    latitude = models.FloatField
    longitude = models.FloatField
    isCoop = models.BooleanField


    
class Equipment(models.Model):
    name = models.CharField(max_length = 30)
    count = models.IntegerField
    equipmentType = models.IntegerField

class CourseTime(models.Model):
    fromHour = models.IntegerField
    fromMinite = models.IntegerField
    toHour = models.IntegerField
    toMinite = models.IntegerField


class Course(models.Model):
    name =models.CharField(max_length = 30)
    week = models.IntegerField
    courseTime = models.ManyToManyField(CourseTime)

class DetailGym(models.Model):
    briefGym = models.ManyToManyField(BriefGym)
    equipments = models.ManyToManyField(quipment)
    courses = models.ManyToManyField(Course)#课程信息
    gymCard = models.ManyToManyField(GymCard)


# class  CardType(Enum):
#    Once = 0;  # 一次 体验卡
#    Month = 1;    # 月卡
#    Quarter = 2;  # 季度卡

class GymCard(models.Model):
    cardType = models.IntegerField #卡类型
    price = models.FloatField


# enum EquipmentType {
#   PAO_BU_JI = 0;  # 跑步机
#   LIN_YU_FANG = 1;      # 淋浴房
# }

# enum Sex{
#   MALE = 0;    # 男性
#   FEMALE = 1;    # 女性
# }


#关于枚举http:#codego.net/1168/ 的方法