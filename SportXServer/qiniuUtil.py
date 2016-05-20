import qiniu
#qiniu 服务端，用户上传key，服务器通过key像qiniu请求储存url

AK = "jKqYBUoUXU7tMf1LneJaBhiLfIkrnHqkmhxVTjz1"
SK = "xwIP5ji4sSErJblNbAIgp47ctH7y8h11LS4kI8dD"

BUCKET = "sportx"

def getDefaultBucketName():
    return BUCKET

def getQiniuTokenWithOutKey():
    return qiniu.Auth(AK, SK).upload_token(BUCKET, expires=36000)

def getQiniuTokenWithOKey(key):
    return qiniu.Auth(AK, SK).upload_token(BUCKET, key=key, expires=36000)

def getBaseUrlByBucketName(bucketName):
    if bucketName == BUCKET:
        return "http://o790nqviz.bkt.clouddn.com/"
    else:
        return ""