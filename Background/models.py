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

#用户表 （用户名，手机号，密码，头像，性别，个性签名，X币数量，注册时间）
class BriefUser(models.Model):
    userid = models.IntegerField(primary_key=True)
    userName = models.CharField(max_length = 30)
    userPhone = models.CharField(max_length = 13)
    userPW = models.CharField(max_length = 30)
    userCover = models.URLField()#image
    userSex = models.BooleanField()#0女1男》？？
    userSign = models.CharField(max_length = 30)
    Xbin = models.IntegerField()
    signTime = models.DateTimeField()


#场馆表 （场馆名字，场馆头像，地址，经度，纬度--浮点6位小数，设备，课程，卡券，简介，添加时间）
class BriefGym(models.Model):
    gymid = models.IntegerField(primary_key=True)
    gymName = models.CharField(max_length = 30)
    gymCover = models.URLField()#image 
    place = models.CharField(max_length = 30)
    latitude = models.FloatField()
    longitude = models.FloatField()
    Equipment = models.ForeignKey(Equipment)
    Course = models.ForeignKey(Course)
    GymCard = models.ForeignKey(GymCard)#名字需要改变
    info = models.CharField(max_length = 300)
    signTime = models.DateTimeField()


#动态表 （动态文字内容，发动态人的id，所在场馆id，所在场馆名字，发送时间）
class Trend(models.Model):
    Trendid = models.IntegerField(primary_key=True)
    Content  =  models.CharField(max_length = 30)
    Userid = models.IntegerField()
    Gymid = models.IntegerField()
    likeUser = models.ForeignKey(BriefUser)#是用外键还是》？
    createTime = models.DateTimeField()
    comment = models.ForeignKey(Comment)
    imgs =  models.URLField()#image 
    #likeCount = models.IntegerField()#用于简化查询
    #commentCount = models.IntergerField()#
#评论表 （评论的文字内容，评论所在的动态id，发表评论的人的id，“所评论的评论”的人的id，所在场馆id，所在场馆名字， 发送时间）？？
#关于外键反查问题的学习 我觉得这个设计有问题
class Comment(models.Model):
    Commentid = models.IntegerField(primary_key=True)
    CommentUser = models.IntegerField()
    Comment = models.CharField(max_length = 300)
    CommentTime = models.DateTimeField()


#点赞表 （动态id，点赞人的id，点赞时间）
class Like(models.Model):
    Likeid = models.IntegerField()
    LikeUser = models.IntegerField()
    LikeTime = models.DateTimeField()

#关注表 （被关注的人的id，关注者的id，关注时间）
class Follow(models.Model):
    Followid = models.ForeignKey(BriefUser)
    Follower = models.ForeignKey(BriefUser)
    FollowTime = models.DateTimeField()
#曾经关注表 （被关注的人的id，关注者的id，关注时间）
class Followrubin(models.Model):
    Followid = models.ForeignKey(BriefUser)
    Follower = models.ForeignKey(BriefUser)
    FollowTime = models.DateTimeField()

#场馆介绍图片表 （场馆id，图片url，添加时间）
class Gyminfo(models.Model):
    gymid = models.ForeignKey(BriefUser)

#动态图片表 （动态id，图片url，图片显示顺序）
class image(models.Model):
    imageid = models.IntegerField(primary_key = True)
    url = models.URLField()
    priority = models.IntegerField()

#X币相关表 （用户id，X币变化量，X币变化原因）
class xbin(models.Model):
    userid = models.ForeignKey(BriefUser)
    detbin = models.IntegerField()
    reason = models.CharField(max_length = 30)


#设备表
class Equipment(models.Model):
    name = models.CharField(max_length = 30,primary_key=True)
    count = models.IntegerField()
    equipmentType = models.IntegerField()

#课程表
class Course(models.Model):
    name =models.CharField(max_length = 30)
    week = models.IntegerField()
    courseTime = models.ForeignKey(CourseTime)
    fromHour = models.IntegerField()
    fromMinite = models.IntegerField()
    toHour = models.IntegerField()
    toMinite = models.IntegerField()

class GymCard(models.Model):
    cardType = models.IntegerField() #卡类型
    price = models.FloatField()

class DetailGym(models.Model):
    briefGym = models.IntegerField()
    equipments = models.ForeignKey(Equipment)
    courses = models.ForeignKey(Course)#课程信息
    gymCard = models.ForeignKey(GymCard)



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