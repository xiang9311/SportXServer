__author__ = '祥祥'

from Background.models import TblTrend, TblTrendImage, TblTrendComment, TblBriefUser, TblTrendComment

import datetime

def getHotTrend():
    """
    返回热门trend列表{trends:[{}]}
    :return:
    """
    trends = []
    now = datetime.datetime.now()
    start = now - datetime.timedelta(days=20)
    tblTrends = TblTrend.objects.filter(createTime__gt=start).order_by('-commentCount')[:10]
    for tblTrend in tblTrends:
        trend = {}
        trend['content'] = tblTrend.content
        trend['createTime'] = str(tblTrend.createTime)[:11]
        images = []
        try:
            tblTrendImages = TblTrendImage.objects.filter(trend = tblTrend).order_by('priority')
            for tblTrendImage in tblTrendImages:
                images.append(tblTrendImage.url)
        except Exception as e:
            pass
        trend['images'] = images
        user = {}
        user['userName'] = tblTrend.createUser.userName
        user['userAvatar'] = tblTrend.createUser.userAvatar
        user['sign'] = tblTrend.createUser.userSign
        trend['user'] = user
        trend['likeCount'] = tblTrend.likeCount
        trend['commentCount'] = tblTrend.commentCount

        comments = []
        try:
            tblComments = TblTrendComment.objects.filter(trend=tblTrend).order_by('commentTime')[:5]
            for tblComment in tblComments:
                comment = {}
                comment['userName'] = tblComment.createUser.userName
                comment['content'] = tblComment.comment
                comments.append(comment)
        except Exception as e:
            pass

        trend['comments'] = comments

        trends.append(trend)
    return trends