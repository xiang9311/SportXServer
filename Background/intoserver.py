#解析器
import Background.proto.common_pb2 as common

#根据视图选择解析器？
# (a object) = common.(a parser)#选择解析器

# (a object).ParseFromString({from a resquet})#解析

# funtion(x)#deal with the parm in object
def RequestCommonParser(resquet):
	RequestCommon = common.RequestCommon()
	RequestCommon.ParseFromString(resquet)
	return RequestCommon
	# RequestCommon.userid
	# RequestCommon.userkey
	# RequestCommon.cmdid
	# RequestCommon.timestamp
	# RequestCommon.version
	# RequestCommon.platform
def ResponseCommon(resquet):
	ResponseCommon = common.ResponseCommon()
	ResponseCommon.ParseFromString(resquet)
	return ResponseCommon

def Trend(resquet):
	Trend = common.Trend()
	Trend.ParseFromString(resquet)
	return Trend

def  BriefUser(resquet):
	BriefUser = common.BriefUser()
	BriefUser.ParseFromString(resquet)
	return BriefUser

def BriefGym(resquet):
	BriefGym = common.BriefGym()
	BriefGym.ParseFromString(resquet)
	return BriefGym

def DetailGym(resquet):
	DetailGym = common.DetailGym()
	DetailGym.ParseFromString(resquet)
	return DetailGym

def Equipment(resquet):
	Equipment = common.Equipment()
	Equipment.ParseFromString(resquet)
	return Equipment

def Course(resquet):
	Course = common.Course()
	Course,ParseFromString(resquet)