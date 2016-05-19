from qiniu import Auth,put_file,etag
import qiniu.config

#qiniu 服务端，用户上传key，服务器通过key像qiniu请求储存url
AK = 'jKqYBUoUXU7tMf1LneJaBhiLfIkrnHqkmhxVTjz1'
SK = 'xwIP5ji4sSErJblNbAIgp47ctH7y8h11LS4kI8dD'
q = Auth(AK,SK)
bucket='sportx'
key =  '4bd91c87gw1ehlszyxo6yj21hc0w0b29.jpg'
token = q.upload_token(bucket,key,3600)
localfile = './213.jpg'
ret,info = put_file(token, key ,localfile)
print(info)
assert ret['key'] == key
assert ret['hash'] == etag(localfile)