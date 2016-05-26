import jpush as jpush
AK = 'bf99a2c43d8865abe4875bb6'
SK = '594a8bba8661d9a037daafd1'

def pushToUser(userId,userName,trendid):
    userId_str = str(userId)
    _jpush = jpush.JPush(AK, SK)
    _jpush.set_logging("DEBUG")
    push = _jpush.create_push()
    push.audience = jpush.audience(
                jpush.alias(userId_str)
            )
    andriod_msg = jpush.android(alert="新消息",title = userName+"评论了你的动态" ,extras = {'trendId':str(trendid)})
    push.notification = jpush.notification(alert="新消息",android=andriod_msg)
    push.platform = jpush.all_
    print (push.payload)
    push.send()