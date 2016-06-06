from Background.models import TblBriefGym
from SportXServer import qiniuUtil, timeUtil, userKeyUtil ,rongcloud, log
from Background.dependency.geohash import encode

def geoadd():
    bgym = TblBriefGym.objects.all()
    for gym in bgym:
        hash = encode(gym.latitude,gym.longitude)
        gym.geohash = hash
        gym.save()

geoadd()


