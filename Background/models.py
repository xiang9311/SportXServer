from django.db import models

# Create your models here.
#request
class RequestCommon(models.Model):
	userid = models.IntegerField
	userkey = models.CharField(max_length = 30)
	cmdid = models.IntegerField
	timestamp = models.DateTimeField
	version =  models.CharField(max_length = 30)
  	platform = models.IntegerField

  #response
class ResponseCommon :
	code = models.IntegerField
	message = models.CharField(max_length = 30)
	cmdid = models.IntegerField
	timestamp = models.DateTimeField
	userid = models.IntegerField

#Trend
class Trend :
	id = models.IntegerField
	briefUser = models.ManyToManyField("BriefUser")
	createTime = models.DateTimeField()
	gymid = models.IntegerField
	gymName =  models.CharField
	content  =  models.CharField
	imgs =  models.ImageField
	likeCount = models.IntegerField
	commentCount = models.IntegerField
	isLiked = models.BooleanField

class Banner :
	#??type    
	# URL = 0;                   // 跳转url
 	#TREND = 1;                 // 跳转动态
	#USER = 2;                  // 用户
	id = models.IntegerField
	coverUrl = models.CharField()
	type = (
		(URL , '0'),
		(TREND , '1'),
		(USER , '2'),
	)
	webUrl = models.CharField()
	trendId = models.IntegerField
	userid = models.IntegerField

class BriefUser :
	userid = models.IntegerField
	userName = models.CharField()
	userAvatar = models.CharField()

class BriefGym :
	id = models.IntegerField
	gymName = models.CharField()
	gymCover = models.ImageField()
	place = models.CharField
	gymAvatar = models.CharField()
	latitude = models.FloatField()
	longitude = models.FloatField()
	isCoop = models.BooleanField

class DetailGym:
	briefGym = models.ManyToManyField("BriefGym")
	equipments = models.ManyToManyField("Equipment")
	 courses = models.ManyToManyField("Course");  // 课程信息
	 gymCard = models.ManyToManyField("GymCards")
	
class Equipment:
	name = models.CharField()
	count = models.IntegerField
	equipmentType = models.ManyToManyField(EquipmentTpye)

class Course :
	name =models.CharField
	week = models.IntegerField
	courseTime = models.ManyToManyField(CourseTime)

class CourseTime :
	fromHour = models.IntegerField
	fromMinite = models.IntegerField
	toHour = models.IntegerField
	toMinite = models.IntegerField

class GymCard :
	cardType = (
		CardType 
		)
	price = models.FloatField
# enum CardType{
# 	Once = 0;     // 一次 体验卡
# 	Month = 1;    // 月卡
# 	Quarter = 2;  // 季度卡
# }

# enum EquipmentType {
# 	PAO_BU_JI = 0;                // 跑步机
# 	LIN_YU_FANG = 1;              // 淋浴房
# }

# enum Sex{
#   MALE = 0;                     // 男性
#   FEMALE = 1;                   // 女性
# }