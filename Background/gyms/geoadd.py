from Background.models import TblBriefGym
from SportXServer import qiniuUtil, timeUtil, userKeyUtil ,rongcloud, log
from Background.dependency.geohash import encode

def geoadd():
    bgym = TblBriefGym.objects.all()
    for gym in bgym:
        gym.equipmentBrief = "大力，四角受，洗浴"
        gym.save()




