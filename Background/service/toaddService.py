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
